import os
import random
import re
import smtplib

import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select , update

from DAO.Auth_Dao import AuthDao
from Database_Models.User_Table import User as UserTable
from database import async_session_maker

load_dotenv ( dotenv_path = 'env/.env' )
ALGORITHM = os.getenv ( 'ALGORITHM' , 'HS256' )
SECRET_KEY = os.getenv ( 'SECRET_KEY' )
REFRESH_SECRET_KEY = os.getenv ( 'REFRESH_SECRET_KEY' )


class EmailDao :
	
	@classmethod
	async def send_email_code ( cls , email ) :
		
		async with async_session_maker ( ) as session :
			query_check_user = select ( UserTable.id_user , UserTable.password_hash , UserTable.login ).where (
				UserTable.email == email
				)
			result = await session.execute ( query_check_user )
			user = result.first ( )
			if not user :
				raise HTTPException ( status_code = 404 , detail = "Пользователь не найден" )
			random_numbers = [ ]
			for n in range ( 6 ) :
				random_numbers.append ( str ( random.randint ( 0 , 9 ) ) )
			codenumber = ''.join ( random_numbers )
			m = re.search ( r'@(.+?)\.' , email )
			
			mailserver = smtplib.SMTP ( os.getenv ( 'SMTP' ) , os.getenv ( 'SMTP_PORT' ) )
			mailserver.ehlo ( )
			mailserver.starttls ( )
			mailserver.ehlo ( )
			mailserver.login ( os.getenv ( 'Login_SMTP' ) , os.getenv ( 'Password_SMTP' ) )
			print ( "Попытка отправки сообщения на почту" )
			message = f'Ваш код подтверждения: {codenumber}'.encode ( 'utf8' )
			mailserver.sendmail ( os.getenv ( 'Login_SMTP' ) , email , message )
			mailserver.quit ( )
			return codenumber
	
	@classmethod
	async def change_password_to_email ( cls , email , password ) :
		async with async_session_maker ( ) as session :
			if not password :
				raise HTTPException ( status_code = 400 , detail = "Отсутствует введённый пароль" )
			if not email :
				raise HTTPException ( status_code = 400 , detail = "Отсутствует email" )
			
			password_hash = bcrypt.hashpw ( password.encode ( ) , bcrypt.gensalt ( ) ).decode ( 'utf-8' )
			
			
			query_change_password = (
				update ( UserTable ).where ( UserTable.email == email )
				.values ( password_hash = password_hash )
			)
			
			await session.execute ( query_change_password )
			await session.commit ( )
			
			
			query_get_user = select ( UserTable ).where ( UserTable.email == email )
			result = await session.execute ( query_get_user )
			user = result.scalars().first()
			
			
			if not user :
				raise HTTPException ( status_code = 404 , detail = "Пользователь не найден" )
			
			
			access_token = await AuthDao.create_jwt_token ( user.id_user )
			refresh_token = await AuthDao.create_refresh_token ( user.id_user )
			
			return { "access_token" : access_token , "refresh_token" : refresh_token }
