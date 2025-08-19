import datetime
import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from sqlalchemy import select , insert , delete , update

# Теперь мы импортируем только сам класс, а не создаем его экземпляр
from DAO.Auth_Dao import AuthDao
from Database_Models.Priority_Tasks_Table import PriorityTasksTable
from Database_Models.Project_Table import ProjectsTable
from Database_Models.Tasks_Table import Tasks_Table
from Database_Models.User_To_Tasks_Table import UserToTasks
from Database_Models.information_status_table import InformationStatusTable
from database import async_session_maker

# Define bearer_scheme once to avoid confusion
bearer_scheme = HTTPBearer ( )

load_dotenv ( dotenv_path = 'env/.env' )
ALGORITHM = os.getenv ( 'ALGORITHM' , 'HS256' )


class TaskDao :
	model = Tasks_Table
	
	@classmethod
	async def createTask (
			cls ,
			jwt_token: str ,
			name: str ,
			description: str ,
			id_project: int ,
			id_priority: int ,
			id_status: int ,
			deadline: datetime
			) -> Tasks_Table :
		async with async_session_maker ( ) as session :
			# Правильный вызов метода класса AuthDao
			payload = await AuthDao.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			
			role = payload.get ( "role" )
			if role != "admin" :
				raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на создание проекта" )
			
			try :
				querry_insert_tasks = (insert ( Tasks_Table ).values (
					id_project = id_project ,
					name = name ,
					description = description ,
					priority = id_priority ,
					status = id_status ,
					deadline = deadline
					))
				await session.execute ( querry_insert_tasks )
				await session.commit ( )
				return await session.scalar (
					select ( Tasks_Table ).where (
						Tasks_Table.name == name ,
						Tasks_Table.id_project == id_project ,
						Tasks_Table.description == description
						)
					)
			except HTTPException as e :
				raise e
	
	@classmethod
	async def getTasks ( cls , jwt_token: str ) :
		async with async_session_maker ( ) as session :
			try :
				# Правильный вызов метода класса AuthDao
				payload = await AuthDao.decode_jwt_token ( jwt_token )
				
				user_id = payload.get ( "user_id" )
				
				if not user_id :
					raise HTTPException ( status_code = 401 , detail = "Недействительный токен" )
				
				querry_select_tasks = (
					select (
						Tasks_Table.id_task.label ( 'id_task' ) ,
						Tasks_Table.name.label ( 'task_name' ) ,
						PriorityTasksTable.information_priority.label ( 'priority' ) ,
						ProjectsTable.id_project.label ( 'id_project' ) ,
						ProjectsTable.name_project.label ( 'project_name' ) ,
						)
					.join ( PriorityTasksTable , PriorityTasksTable.id_priority == Tasks_Table.priority )
					.join ( InformationStatusTable , InformationStatusTable.id_information == Tasks_Table.status )
					.join ( UserToTasks , UserToTasks.id_task == Tasks_Table.id_task )
					.join ( ProjectsTable , Tasks_Table.id_project == ProjectsTable.id_project )
					.filter ( UserToTasks.id_user == user_id )
				)
				
				result = await session.execute ( querry_select_tasks )
				tasks = result.mappings ( ).all ( )
				print ( tasks )
				return tasks
			
			except HTTPException as e :
				
				raise e
			except Exception as e :
				print ( f"Ошибка вывода задач: {e}" )
				raise HTTPException ( status_code = 500 , detail = f"Ошибка вывода задач: {str ( e )}" )
	
	@classmethod
	async def deleteTask ( cls , jwt_token: str , id_task: int ) :
		async with async_session_maker ( ) as session :
			payload = await AuthDao.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			
			role = payload.get ( "role" )
			result = await session.execute ( select ( Tasks_Table ).where ( Tasks_Table.id == id_task ) )
			task = result.scalar_one_or_none ( )
			
			if task is None :
				raise HTTPException ( status_code = 404 , detail = "Задача не найдена" )
			
			if role != "admin" :
				raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на удаление задачи" )
			
			try :
				querry_delete_tasks = (
					delete ( Tasks_Table ).filter ( Tasks_Table.id == id_task )
				)
				await session.execute ( querry_delete_tasks )
				await session.commit ( )
				return { "message" : f"Задача с id {id_task} успешно удалена." }
			except Exception as e :
				raise HTTPException ( status_code = 500 , detail = f"Ошибка удаления задачи: {str ( e )}" )
	
	@classmethod
	async def updateTask (
			cls ,
			jwt_token: str ,
			id_task: int ,
			name: Optional [ str ] = None ,
			description: Optional [ str ] = None ,
			id_status: Optional [ int ] = None ,
			id_priority: Optional [ int ] = None ,
			) :
		async with async_session_maker ( ) as session :
			payload = await AuthDao.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			
			role = payload.get ( "role" )
			if role != "admin" :
				raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на изменение задачи" )
			
			result = await session.execute ( select ( Tasks_Table ).where ( Tasks_Table.id == id_task ) )
			task = result.scalar_one_or_none ( )
			
			if task is None :
				raise HTTPException ( status_code = 404 , detail = "Задача не найдена" )
			
			updates = { }
			if name is not None :
				updates [ "name" ] = name
			if description is not None :
				updates [ "description" ] = description
			if id_status is not None :
				updates [ "status" ] = id_status
			if id_priority is not None :
				updates [ "priority" ] = id_priority
			
			if not updates :
				raise HTTPException ( status_code = 400 , detail = "Нет полей для обновления" )
			
			stmt = (
				update ( Tasks_Table )
				.where ( Tasks_Table.id == id_task )
				.values ( **updates )
				.execution_options ( synchronize_session = "fetch" )
			)
			await session.execute ( stmt )
			await session.commit ( )
			
			result = await session.execute ( select ( Tasks_Table ).where ( Tasks_Table.id == id_task ) )
			updated_task = result.scalar_one ( )
			return updated_task
