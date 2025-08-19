import os
import random
import re
import smtplib

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select

from Database_Models.User_Table import User as UserTable
from database import async_session_maker

load_dotenv ( dotenv_path = 'env/.env' )
class EmailDao :
	
	@classmethod
	async def send_email_code ( cls , email ) :
		print(os.environ[ 'SMTP' ])
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
			print("Попытка отправки сообщения на почту")
			message = f'Ваш код подтверждения: {codenumber}'.encode ('utf8')
			mailserver.sendmail ( os.getenv ( 'Login_SMTP' ) , email , message )
			mailserver.quit ( )
			return codenumber
