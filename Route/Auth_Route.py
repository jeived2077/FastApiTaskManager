from fastapi import APIRouter , HTTPException , Depends
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from pydantic import BaseModel , Field , field_validator
from sqlalchemy import select

from DAO.Auth_Dao import AuthDao as Auth_Dao
from Database_Models.User_Table import User as UserTable
from database import async_session_maker

router = APIRouter ( prefix = "/auth" , tags = [ "Авторизация и регистрация" ] )

security = HTTPBearer ( )


class SchemaRegistrationUser ( BaseModel ) :
	login: str = Field ( ... , description = "Данный логин занят" )
	password: str = Field (
		min_length = 8 ,
		max_length = 20 ,
		pattern = r"[A-Za-z\\d@$!%*?&\\-]{8,20}" ,
		description = "Пароль должен быть длиной от 8 до 20 символов, содержать буквы, цифры и специальные символы"
		)
	
	email: str = Field ( description = "Данная электронная почта занята" )
	
	@field_validator ( "password" )
	def validate_password ( cls , password: str ) :
		if not any ( c.isalpha ( ) for c in password ) :
			raise ValueError ( "Пароль должен содержать хотя бы одну букву" )
		if not any ( c.isdigit ( ) for c in password ) :
			raise ValueError ( "Пароль должен содержать хотя бы одну цифру" )
		return password


@router.post ( "/registr" , summary = "Регистрация" )
async def registration ( request: SchemaRegistrationUser ) :
	try :
		async with async_session_maker ( ) as session :
			
			query_check_login = select ( UserTable.id_user ).where ( UserTable.login == request.login )
			result = await session.execute ( query_check_login )
			if result.first ( ) :
				raise HTTPException ( status_code = 400 , detail = "Пользователь с таким логином уже существует" )
			
			query_check_email = select ( UserTable.id_user ).where ( UserTable.email == request.email )
			result = await session.execute ( query_check_email )
			if result.first ( ) :
				raise HTTPException (
					status_code = 400 , detail = "Пользователь с такой электронной почтой уже существует"
					)
		
		user_data = {
			"login" : request.login ,
			"password" : request.password ,
			"email" : request.email ,
			
			}
		
		return await Auth_Dao.registration_user ( **user_data )
	except Exception as e :
		raise HTTPException ( status_code = 500 , detail = f"Ошибка при регистрации: {str ( e )}" )


class LoginRequest ( BaseModel ) :
	login: str
	password: str


@router.post ( "/login" , summary = "Авторизация" )
async def authorization ( request: LoginRequest ) :
	return await Auth_Dao.login_user ( request.login , request.password )


@router.post ( "/refresh" )
async def refresh ( credentials: HTTPAuthorizationCredentials = Depends ( security ) ) :
	refresh_token = credentials.credentials
	return await Auth_Dao.refresh_access_token ( refresh_token )


# @router.push ( "/change_password" , summary = "Изменение пароля" )
# async def change_password ( jwt_token: str , password: str ) :
# 	user_data = {
# 		"jwt_token" : jwt_token ,
# 		"password" : password ,
# 		}
#
# 	return await Auth_Dao.change_password ( **user_data )
#
#
# @router.push ( "/change_email" , summary = "Измененеие электронной почты" )
# async def change_email ( jwt_token: str , email: str  ) :
# 	user_data = {
# 		"jwt_token" : jwt_token ,
# 		"email" : email.check_email(email) ,
# 		}
#
# 	return await Auth_Dao.change_avatar ( **user_data )
#
#
#
# @router.push ( "/change_avatar" , summary = "Изменение изображение пользователя" )
# async def change_avatar ( jwt_token: str , photo: bytes ) :
# 	user_data = {
# 		"jwt_token" : jwt_token ,
# 		"photo" : photo ,
# 		}
#
# 	return await Auth_Dao.change_avatar ( **user_data )
#
class PasswordChangeRequest ( BaseModel ) :
	email: str
	password: str = Field (
		min_length = 8 ,
		max_length = 20 ,
		pattern = r"[A-Za-z\\d@$!%*?&\\-]{8,20}" ,
		description = "Пароль должен быть длиной от 8 до 20 символов, содержать буквы, цифры и специальные символы"
		)



