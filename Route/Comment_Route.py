from fastapi import APIRouter
from pydantic import BaseModel

from DAO.Comment_Dao import CommentsDAO

router = APIRouter ( prefix = "/comments" , tags = [ "Коментарии" ] )


class SchemaCreateComment ( BaseModel ) :
	id_commit: str
	jwt_Token: str
	text_comment: str


@router.get ( "/", summary="Вывести Коментарии" )
async def listcommets ( ) :
	
	return await CommentsDAO.list_commets()


@router.post ( "/create" , response_model = SchemaCreateComment, summary="Создать комментарий" )
async def createcommets ( ) :
	return await CommentsDAO.add_commets ( )
	
	
	
	
	
	pass


class SchemaDeleteComment ( BaseModel ) :
	id_commit: str
	jwt_Token: str


@router.delete ( "/delete/{commets_id}" , response_model = SchemaDeleteComment, summary="Удалить комментарий" )
def deletecommets ( commets_id: int ) :
	pass


class SchemaChangeCommets ( BaseModel ) :
	commets_id: int
	jwt_token: str
	ChangeText: str


@router.patch ( "/change/{commets_id}" , response_model = SchemaChangeCommets, summary="Изменить комментарий" )
def changecommets () :
	pass


@router.get ( "/detail{commets_id}" , include_in_schema = False, summary="Подробная информация комментарий" )
def detailcommets ( commets_id: int ) :
	pass
