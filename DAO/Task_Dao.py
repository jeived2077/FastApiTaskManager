import os
from operator import truediv

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import select , Update

from DAO.Auth_Dao import AuthDao
from Database_Models.Comments_Table import CommentsTable
from Database_Models.Detail_Commets_Table import NestedCommentsTable
from Database_Models.Priority_Tasks_Table import PriorityTasksTable
from Database_Models.Project_Table import ProjectsTable
from Database_Models.Tasks_Table import Tasks_Table
from Database_Models.User_Table import User
from Database_Models.User_To_Project_Table import UserToProject
from Database_Models.User_To_Tasks_Table import UserToTasks
from Route.Task_Route import ResponseCommentsModel , ResponseNestedCommentsModel , TasksAndCommentsResponse
from database import async_session_maker

bearer_scheme = HTTPBearer ( )

load_dotenv ( dotenv_path = 'env/.env' )
ALGORITHM = os.getenv ( 'ALGORITHM' , 'HS256' )


class TaskDao :
	model = Tasks_Table
	#Получение задач и проектов
	@classmethod
	async def gettasksandproject (
			cls , jwt_token: str , priority: str = None , filter: str = None , status_project: str = None ,
			status_tasks: str = None
			) :
		async with async_session_maker ( ) as session :
			try :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				
				if not user_id :
					raise HTTPException ( status_code = 401 , detail = "Недействительный токен" )
				querry_select_list_task = (select (
					Tasks_Table.id_task.label ( 'Id_Task' ) , Tasks_Table.name.label ( 'Name_Task' ) ,
					Tasks_Table.deadline.label ( 'dealine_At' ) , Tasks_Table.created_at.label ( 'created_At' ) ,
					User.login.label ( 'created_By' ) ,
					PriorityTasksTable.information_priority.label ( 'name_priority' ) , ).join (
					UserToTasks , UserToTasks.id_task == Tasks_Table.id_task
					).join (
					User , UserToTasks.id_user == User.id_user
					).join (
					PriorityTasksTable , PriorityTasksTable.id_priority == Tasks_Table.priority
					).filter ( UserToTasks.id_user == user_id ))
				querry_select_priority_task = (
					select ( PriorityTasksTable.information_priority.label ( 'name_priority' ) ).distinct ( ))
				querry_select_list_project = (select (
					ProjectsTable.id_project.label ( 'Id_Project' ) ,
					ProjectsTable.name_project.label ( 'Name_Project' ) ,
					ProjectsTable.created_at.label ( 'created_At' ) ,
					
					User.login.label ( 'created_By' ) , ).join (
					UserToProject , UserToProject.id_project == ProjectsTable.id_project
					).join (
					User , User.id_user == UserToProject.id_user
					).filter (
					UserToProject.id_user == user_id
					).distinct ( ))
				if filter :
					match (filter) :
						case ("По дате создания") :
							querry_select_list_task = querry_select_list_task.order_by ( Tasks_Table.created_at )
						
						case ("По дате сдачи") :
							querry_select_list_task = querry_select_list_task.order_by ( Tasks_Table.deadline )
						case ("По дате приоритета") :
							querry_select_list_task = querry_select_list_task.order_by (
								PriorityTasksTable.id_priority
								)
				if status_tasks :
					querry_select_list_task = querry_select_list_task.order_by ( Tasks_Table.created_at )
				if status_project :
					querry_select_list_task = querry_select_list_task.order_by ( Tasks_Table.created_at )
				if priority :
					select (
						PriorityTasksTable.information_priority.label ( 'name_priority' )
						).distinct ( )
				result_priority = await session.execute ( querry_select_priority_task )
				result_project = await session.execute ( querry_select_list_project )
				project = result_project.mappings ( ).all ( )
				result_task = await session.execute ( querry_select_list_task )
				tasks = result_task.mappings ( ).all ( )
				priority = result_priority.mappings ( ).all ( )
				
				return {
					"priorities" : [ dict ( p ) for p in priority ] ,
					"tasks" : [ dict ( task ) for task in tasks
					            
					            ] ,
					"projects" : [
						
						dict ( project ) for project in project
						
						]
					}
			
			except HTTPException as e :
				raise e
			except Exception as e :
				print ( f"Ошибка вывода задач: {e}" )
				raise HTTPException ( status_code = 500 , detail = f"Ошибка вывода задач: {str ( e )}" )
	@classmethod
	async def change_status_task( cls, jwt_token: str , status: int = None, id_task: int = None, ):
		async with async_session_maker() as session:
			try:
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 401 , detail = "Недействительный токен" )
				querry_change_status_task = (
					Update (Tasks_Table).where (Tasks_Table.id_project == id_task).values (status = status )
				)
				result_change = await session.execute ( querry_change_status_task )
				if result_change :
					return True
				else:
					return False
				
			except HTTPException as e :
				raise HTTPException ( status_code = 500 , detail = f"Ошибка изменения статуса задачи: {str ( e )}" )
			except Exception as e :
				print ( f"Ошибка изменения статуса задачи: {e}" )
				raise HTTPException ( status_code = 500 , detail = f"Ошибка изменения статуса задачи: {str ( e )}" )
	
	@classmethod
	async def task_detail_information ( cls , jwt_token: str , id_task: int = None ) :
		try :
			async with async_session_maker ( ) as session :
				
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 401 , detail = "Недействительный токен" )
				
			
				query_task = select ( Tasks_Table ).where ( Tasks_Table.id_task == id_task )
				result_task = await session.execute ( query_task )
				
				
				task = result_task.scalars ( ).first ( )
				
				if not task :
					raise HTTPException ( status_code = 404 , detail = "Задача не найдена" )
				
				
				comments_list_response = [ ]
				
				
				query_comments = (
					select ( CommentsTable , User.login , User.photo )
					.join ( User , User.id_user == CommentsTable.id_user )
					.where ( CommentsTable.id_task == task.id_task )
				)
				result_comments = await session.execute ( query_comments )
				
				
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
				
				
				task_response = TasksAndCommentsResponse (
					Id_Task = task.id_task ,
					Name_Task = task.name_task ,
					created_At = task.created_at ,
					dealine_At = task.dealine_at ,
					created_By = task.created_by ,
					name_priority = task.name_priority ,
					
					comments = comments_list_response
					)
				
				
				return task_response
		
		except HTTPException as e :
			raise e
		except Exception as e :
			print ( f"Ошибка получения информации о задаче: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Внутренняя ошибка сервера: {str ( e )}" )