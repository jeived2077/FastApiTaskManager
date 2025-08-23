from fastapi import APIRouter
from pydantic import Field , BaseModel , field_validator

from DAO.Email_Dao import EmailDao as Email_Dao

router = APIRouter ( prefix = "/email" , tags = [ "Электронная почта" ] )


@router.get ( "/send_email_to_code" , summary = "Отправить код" )
async def send_email_to_code ( email: str ) :
	return await Email_Dao.send_email_code ( email )


class PasswordChangeRequest ( BaseModel ) :
	email: str
	password: str = Field (
		min_length = 8 ,
		max_length = 20 ,
		pattern = r"[A-Za-z\\d@$!%*?&\\-]{8,20}" ,
		description = "Пароль должен быть длиной от 8 до 20 символов, содержать буквы, цифры и специальные символы"
		)
	
	@field_validator ( "password" )
	def validate_password ( cls , password: str ) :
		if not any ( c.isalpha ( ) for c in password ) :
			raise ValueError ( "Пароль должен содержать хотя бы одну букву" )
		if not any ( c.isdigit ( ) for c in password ) :
			raise ValueError ( "Пароль должен содержать хотя бы одну цифру" )
		return password


@router.post ( "/change_password_filter_email" , summary = "Изменения пароля по email" )
async def change_password_email ( request: PasswordChangeRequest ) :
	return await Email_Dao.change_password_to_email ( request.email , request.password )
