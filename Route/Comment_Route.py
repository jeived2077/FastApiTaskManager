from fastapi import APIRouter , Depends
from fastapi.security import HTTPAuthorizationCredentials

from DAO.Comment_Dao import CommentsDAO
from DAO.Task_Dao import bearer_scheme
from Response_Request_Model.Comment_Response_Request_Model import RequestAddComments, RequestDeleteComment, RequestChangeComments
router = APIRouter ( prefix = "/comments" , tags = [ "Коментарии" ] )


@router.post ( "/create"  , summary = "Создать комментарий" )
async def create_comment ( request_add_comment: RequestChangeComments,
		credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme )
		) :
	jwt_token = credentials.credentials
	return await CommentsDAO.add_commets ( jwt_token = jwt_token , comment = request_add_comment.text , Photo = request_add_comment.Photo )


@router.delete ( "/delete/{id_comment}"  , summary = "Удалить комментарий" )
async def delete_comment (request_delete: RequestDeleteComment  , credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme ) , ) :
	jwt_token = credentials.credentials
	return await CommentsDAO.delete_commets(jwt_token = jwt_token, id_comment = request_delete.id_commit)


@router.put ( "/change/{id_comment}"  , summary = "Изменить комментарий" )
async def change_comment (request_change:
RequestChangeComments, credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme )  ) :
	jwt_token = credentials.credentials
	return await CommentsDAO.update_comments ( jwt_token = jwt_token , text_comment = request_change.text , Photo = request_change.Photo )


@router.put ( '/change_nested/{id_comment}' , summary = "Изменение вложенных комментарий" )
async def change_nested_comment (request_change: RequestChangeComments, credentials: HTTPAuthorizationCredentials =
Depends ( bearer_scheme )  ) :
	jwt_token = credentials.credentials
	return await CommentsDAO.update_nested_comment ( jwt_token = jwt_token, id_comment = request_change.id_comment ,
	text_comment = request_change.text_comment , photo = request_change.photo )
		
		
		
	


@router.delete ( '/delete_nested/{id_comment}' , summary = "Удаление вложенных комментарий" )
async def delete_nested_comment (request_delete: RequestDeleteComment, credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme )
 ) :
	jwt_token = credentials.credentials
	return await CommentsDAO.delete_nested_comment ( jwt_token = jwt_token, id_comment = request_delete.id_comment , )


@router.post ( '/add_nested' , summary = "Добавление вложенных комментарий" )
async def add_nested_comment (request_add: RequestAddComments ,credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme ) ) :
	jwt_token = credentials.credentials
	return await CommentsDAO.add_nested_comment ( jwt_token = jwt_token, text_comment = request_add.text_comment , photo = request_add.photo )



@router.get ( '/' , summary = "Вывод всех комментарий вместе с вложенными" )
async def list_comments ( id_task: str, credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme ) ) :
	jwt_token = credentials.credentials
	return await CommentsDAO.list_comments_to_task ( jwt_token = jwt_token, id_task = id_task )
