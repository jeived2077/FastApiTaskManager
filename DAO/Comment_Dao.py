from sqlalchemy import select , insert , delete , update

from DAO.Auth_Dao import AuthDao
from Database_Models import Detail_Commets_Table as Comments_Detail
from fastapi import HTTPException
from Database_Models.Comments_Table import CommentsTable
from Database_Models.Detail_Commets_Table import NestedCommentsTable
from Database_Models.User_Table import User
from Database_Models.information_status_table import InformationStatusTable
from Response_Request_Model.Comment_Response_Request_Model import ResponseNestedCommentsModel , ResponseCommentsModel
from database import async_session_maker


class CommentsDAO :
	
	
	
	
	@classmethod
	async def add_commets ( cls, jwt_token: str, comment : str = None, Photo: bytes = None ) :
		try:
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				query = (
					insert ( CommentsTable )
					.values ( id_user = user_id , text_comment = comment )
				)
				result = await session.execute ( query )
				
				return True
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в добавлении комментария: {str ( e )}" )
	
	@classmethod
	async def delete_commets ( cls , id_comment: str, jwt_token: str ) :
		try:
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				query = (delete ( CommentsTable ).where ( CommentsTable.id_comment == id_comment ))
				result = await session.execute ( query )
				return result.scalars ( ).all ( )
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка удаления комментария: {str ( e )}" )
	
	@classmethod
	async def update_comments ( cls , id_comment: str  , jwt_token: str, Photo: bytes = None, text_comment: str = None ) :
		try:
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				query = (update(CommentsTable).values ( text_comment = text_comment , is_edited = True ).where (
					CommentsTable.id_comment == id_comment, CommentsTable.id_user == user_id
					))
				result = await session.execute ( query )
				if not result :
					raise HTTPException ( status_code = 404 , detail = "Не найден комментарий привязанный к вашему аккаунту" )
				return result.scalars ( ).all ( )
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в изменении комментария: {str ( e )}" )
	
	@classmethod
	async def update_nested_comment ( cls, jwt_token: str, id_comment: str = None, text_comment: str = None, photo: bytes  = None ) :
		try :
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				query = (update ( NestedCommentsTable ).values ( text_comment = text_comment , photo = photo, is_edited = True ).where (
					CommentsTable.id_comment == id_comment , CommentsTable.id_user == user_id
					))
				result = await session.execute ( query )
				if not result :
					raise HTTPException (
						status_code = 404 , detail = "Не найден комментарий привязанный к вашему аккаунту"
						)
				return result.scalars ( ).all ( )
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в изменении комментария: {str ( e )}" )
	
	@classmethod
	async def delete_nested_comment ( cls , id_comment: str, jwt_token: str ) :
		try :
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				query = (delete ( NestedCommentsTable ).where ( CommentsTable.id_comment == id_comment ))
				result = await session.execute ( query )
				return result.scalars ( ).all ( )
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка удаления комментария: {str ( e )}" )
	
	@classmethod
	async def add_nested_comment ( cls, jwt_token: str, text_comment: str, photo: bytes  ) :
		try :
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				query = (
					insert ( NestedCommentsTable )
					.values ( id_user = user_id , text_comment = text_comment, photo = photo )
				)
				result = await session.execute ( query )
				
				return True
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в добавлении комментария: {str ( e )}" )
		
	@classmethod
	async def list_comments_to_task ( cls , jwt_token: str, id_task: str ) :
		try :
			async with async_session_maker ( ) as session :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				querry_status = (
					select ( InformationStatusTable )
				)
				result_status = await session.execute ( querry_status )
				data_status = result_status.scalars ( ).all ( )
				
				query_comments = (
					select ( CommentsTable , User.login , User.photo )
					.join ( User , User.id_user == CommentsTable.id_user )
					.where ( CommentsTable.id_task == id_task )
				)
				result_comments = await session.execute ( query_comments )
				comments_list_response = [ ]
				for comment_row in result_comments.mappings ( ).all ( ) :
					comment_obj = comment_row.CommentsTable
					comment_id = comment_obj.id_comment
					
					nested_comments_list_response = [ ]
					
					query_nested = (
						select ( NestedCommentsTable , User.login , User.photo )
						.join ( User , User.id_user == NestedCommentsTable.id_user )
						.where ( NestedCommentsTable.id_comment == comment_id )
					)
					result_nested = await session.execute ( query_nested )
					
					nested_comments_list_response = [ ]
					for nested_row in result_nested.mappings ( ).all ( ) :
						nested_obj = nested_row.NestedCommentsTable
						
						nested_model = ResponseNestedCommentsModel (
							id_comment = nested_obj.id_nestcomm ,  # Вероятно, здесь PK
							text_comment = nested_obj.text_comment ,
							created_At = nested_obj.created_At ,
							created_By = nested_obj.created_by ,
							loginUsername = nested_row.login ,
							photo = nested_row.photo ,
							)
						nested_comments_list_response.append ( nested_model )
					comment_model = ResponseCommentsModel (
						id_comment = comment_id ,
						text_comment = comment_obj.text_comment ,
						created_At = comment_obj.created_At ,
						created_By = comment_obj.created_by ,
						loginUsername = comment_row.login ,
						photo = comment_row.photo ,
						
						nested_comments = nested_comments_list_response
						)
					comments_list_response.append ( comment_model )
					return comment_list_response
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка вывода задач: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Ошибка в добавлении комментария: {str ( e )}" )