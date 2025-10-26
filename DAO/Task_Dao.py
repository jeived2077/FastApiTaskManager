import os

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
from Database_Models.information_status_table import InformationStatusTable
from Response_Request_Model.Task_Response_Request_Model import (
	ResponseCommentsModel , ResponseNestedCommentsModel , TasksAndCommentsResponse ,
	StatusModelReponse ,
	)
from database import async_session_maker

bearer_scheme = HTTPBearer ( )

load_dotenv ( dotenv_path = 'env/.env' )
ALGORITHM = os.getenv ( 'ALGORITHM' , 'HS256' )


class TaskDao :
	model = Tasks_Table
	
	# Получение задач и проектов
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
	async def change_status_task ( cls , jwt_token: str , status: int = None , id_task: int = None , ) :
		async with async_session_maker ( ) as session :
			try :
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				if not status :
					raise HTTPException ( status_code = 404 , detail = "Отсутсвует входящие данные для задачи" )
				if not user_id :
					raise HTTPException ( status_code = 401 , detail = "Недействительный токен" )
				querry_change_status_task = (
					Update ( Tasks_Table ).where ( Tasks_Table.id_project == id_task ).values ( status = status )
				)
				result_change = await session.execute ( querry_change_status_task )
				if not result_change :
					raise HTTPException ( status_code = 404 , detail = "Отсутсвует задача" )
				
				return True
				
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
				
		
				status_list_response = [ ]
				querry_status = (
					select ( InformationStatusTable )
				)
				result_status = await session.execute ( querry_status )
				data_status = result_status.scalars ( ).all ( )
				
					
				status_model = StatusModelReponse (
					id_status = data_status.id_status ,
					name_status = data_status.name_status
					)
				status_list_response.append ( status_model )
				
	
				task_response = TasksAndCommentsResponse (
					Id_Task = task.id_task ,
					Name_Task = task.name_task ,
					created_At = task.created_at ,
					dealine_At = task.dealine_at ,
					created_By = task.created_by ,
					name_priority = task.name_priority ,
					status = status_list_response
					
					)
				
				return task_response
		
		except HTTPException as e :
			raise HTTPException ( status_code = 500 , detail = f"Ошибка по запросу: {str ( e )}" )
		except Exception as e :
			print ( f"Ошибка получения информации о задаче: {e}" )
			raise HTTPException ( status_code = 500 , detail = f"Внутренняя ошибка сервера: {str ( e )}" )
