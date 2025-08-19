from fastapi import APIRouter
from DAO.Email_Dao import EmailDao as Email_Dao
router = APIRouter ( prefix = "/email" , tags = [ "Электронная почта" ] )


@router.get ( "/send_email_to_code" , summary = "Отправить код" )
async def send_email_to_code ( email: str ) :
	return await Email_Dao.send_email_code ( email )
