from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter ( prefix = "/project" , tags = [ "Проекты" ] )



@router.get ( "/", summary="Вывести проекты")
def listprojects ( ) :
	
	pass


@router.post ( "/create", summary="Создать проект")
def createproject ( ) :
	
	pass


@router.delete ( "/delete/{project_id}" , include_in_schema = False, summary="Удалить проект" )
def deleteproject ( project_id: int ) :
	
	pass


@router.patch ( "/change/{project_id}" , include_in_schema = False, summary="Изменить проект" )
def changeproject ( project_id: int ) :
	
	pass


@router.get ( "/detail/{project_id}" , include_in_schema = False, summary="Подробнее проект" )
def detailproject ( project_id: int ):

	pass
