import os
from datetime import datetime , timedelta , timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select , insert , update

from Database_Models.User_Table import User as UserTable
from database import async_session_maker

load_dotenv ( dotenv_path = 'env/.env' )
ALGORITHM = os.getenv ( 'ALGORITHM' , 'HS256' )
SECRET_KEY = os.getenv ( 'SECRET_KEY' )
REFRESH_SECRET_KEY = os.getenv ( 'REFRESH_SECRET_KEY' )


class AuthDao :
	model = UserTable
	
	
	
	@classmethod
	async def registration_user ( cls , login: str , password: str , email: str) :
		password_hash = bcrypt.hashpw ( password.encode ( ) , bcrypt.gensalt ( ) ).decode ( 'utf-8' )
		role = "member"
		async with async_session_maker ( ) as session :
			query = insert ( UserTable ).values (
				login = login ,
				password_hash = password_hash ,
				email = email ,
				role = role ,
				)
			result = await session.execute ( query )
			user_id = result.inserted_primary_key [ 0 ]
			await session.commit ( )
			
			access_token = await cls.create_jwt_token ( user_id )
			refresh_token = await cls.create_refresh_token ( user_id )
			
			return { "access_token" : access_token , "refresh_token" : refresh_token }
	
	@classmethod
	async def create_jwt_token ( cls , user_id: int ) -> str :
		async with async_session_maker ( ) as session :
			select_data_to_jwt = select (
				UserTable.role , UserTable.login , UserTable.photo
				).where ( UserTable.id_user == user_id )
			
			result = await session.execute ( select_data_to_jwt )
			user_data = result.first ( )
			
			if not user_data :
				raise ValueError ( "Нету данных о пользователе в базе данных" )
			
			
			current_time = datetime.now ( timezone.utc )
			expiration_time = current_time + timedelta ( minutes = 30 )
			
			payload = {
				"user_id" : user_id ,
				"role" : user_data.role ,
				"login" : user_data.login ,
				"photo" : user_data.photo ,
				"iat" : int ( current_time.timestamp ( ) ) ,
				"exp" : int ( expiration_time.timestamp ( ) )
				}
			
			token = jwt.encode ( payload , SECRET_KEY , algorithm = ALGORITHM )
			
			return token
	
	@classmethod
	async def create_refresh_token ( cls , user_id: int ) -> str :
		current_time = datetime.now ( timezone.utc )
		payload = {
			"user_id" : user_id ,
			"iat" : int ( current_time.timestamp ( ) ) ,
			"exp" : int ( (current_time + timedelta ( days = 7 )).timestamp ( ) )
			}
		token = jwt.encode ( payload , REFRESH_SECRET_KEY , algorithm = ALGORITHM )
		return token
	
	@classmethod
	async def refresh_access_token ( cls , refresh_token: str ) :
		try :
			
			payload = jwt.decode ( refresh_token , REFRESH_SECRET_KEY , algorithms = [ ALGORITHM ] )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 401 , detail = "Invalid refresh token" )
			
			access_token = await cls.create_jwt_token ( user_id )
			return { "access_token" : access_token }
		except jwt.ExpiredSignatureError :
			raise HTTPException ( status_code = 401 , detail = "Refresh token expired" )
		except jwt.InvalidTokenError :
			raise HTTPException ( status_code = 401 , detail = "Invalid refresh token" )
	
	@classmethod
	async def login_user ( cls , login: str , password: str ) :
		async with async_session_maker ( ) as session :
			query_check_user = select ( UserTable.id_user , UserTable.password_hash , UserTable.login ).where (
				UserTable.login == login
				)
			result = await session.execute ( query_check_user )
			user = result.first ( )
			if not user :
				raise HTTPException ( status_code = 404 , detail = "Пользователь не найден" )
			
			if not bcrypt.checkpw ( password.encode ( 'utf-8' ) , user.password_hash.encode ( 'utf-8' ) ) :
				raise HTTPException ( status_code = 400 , detail = "Неверный пароль" )
			
			access_token = await cls.create_jwt_token ( user.id_user )
			refresh_token = await cls.create_refresh_token ( user.id_user )
			return { "access_token" : access_token , "refresh_token" : refresh_token }
	
	@classmethod
	async def decode_jwt_token ( cls , token: str ) -> dict :
		try :
			payload = jwt.decode (
				token ,
				SECRET_KEY ,
				algorithms = [ ALGORITHM ] ,
				options = { "verify_exp" : True }
				)
			if "user_id" not in payload :
				raise HTTPException ( status_code = 401 , detail = "Недействительный токен: user_id отсутствует" )
			
			return payload
		except jwt.ExpiredSignatureError :
			raise HTTPException ( status_code = 401 , detail = "Токен истек" )
		except jwt.InvalidTokenError as e :
			raise HTTPException ( status_code = 401 , detail = f"Недействительный токен: {e}" )
		except Exception as e :
			raise HTTPException ( status_code = 401 , detail = f"Ошибка декодирования токена: {e}" )
	@classmethod
	async def change_password ( cls , jwt_token: str , password: str ) -> str :
		async with async_session_maker ( ) as session :
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			
			if not password :
				raise HTTPException ( status_code = 400 , detail = "Отсутствует пароль для изменения" )
			
			password_hash = bcrypt.hashpw ( password.encode ( ) , bcrypt.gensalt ( ) ).decode ( 'utf-8' )
			query_change_password = (
				update ( UserTable )
				.where ( UserTable.id_user == user_id )
				.values ( password_hash = password_hash )
			)
			await session.execute ( query_change_password )
			await session.commit ( )
			return "Пароль изменён"
	
	@classmethod
	async def change_avatar ( cls , jwt_token: str , avatar: bytes ) -> str :
		async with async_session_maker ( ) as session :
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			if not avatar :
				raise HTTPException ( status_code = 400 , detail = "Отсутствует аватар" )
			
			query_change_avatar = (
				update ( UserTable )
				.where ( UserTable.id_user == user_id )
				.values ( photo = avatar )
			)
			await session.execute ( query_change_avatar )
			await session.commit ( )
			return "Фотография изменена"


