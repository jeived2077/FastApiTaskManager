import os

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy import select

from DAO.Auth_Dao import AuthDao
from Database_Models.Priority_Tasks_Table import PriorityTasksTable
from Database_Models.Project_Table import ProjectsTable
from Database_Models.Tasks_Table import Tasks_Table
from Database_Models.User_Table import User
from Database_Models.User_To_Project_Table import UserToProject
from Database_Models.User_To_Tasks_Table import UserToTasks
from database import async_session_maker

bearer_scheme = HTTPBearer ( )

load_dotenv ( dotenv_path = 'env/.env' )
ALGORITHM = os.getenv ( 'ALGORITHM' , 'HS256' )


class TaskDao :
	model = Tasks_Table
	
	@classmethod
	async def gettasksandproject ( cls , jwt_token: str , priority: str = None , filter: str = None, status_project: str = None, status_tasks: str = None) :
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
				if status_tasks:
					querry_select_list_task = querry_select_list_task.order_by ( Tasks_Table.created_at )
				if status_project:
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
					"priorities" : [ dict ( p ) for p in priority ] , "tasks" : [ dict ( task ) for task in tasks ] ,
					"projects" : [ dict ( project ) for project in project ]
					}
			
			except HTTPException as e :
				raise e
			except Exception as e :
				print ( f"Ошибка вывода задач: {e}" )
				raise HTTPException ( status_code = 500 , detail = f"Ошибка вывода задач: {str ( e )}" )
