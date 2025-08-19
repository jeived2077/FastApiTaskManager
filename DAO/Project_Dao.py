from fastapi import HTTPException
from sqlalchemy import select , insert , delete , exc, update

from Database_Models.Project_Table import ProjectsTable
from Database_Models.User_To_Project_Table import UserToProject
from database import async_session_maker


class ProjectDa0 :
	model = ProjectsTable
	
	@classmethod
	async def createProject (
			cls , jwt_token: str , name: str , description: str , limit_task: int , status_project: int
			) -> ProjectsTable :
		async with async_session_maker ( ) as session :
			
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			role = payload.get ( "role" )
			if role != "admin" :
				raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на создание проекта" )
			try :
				querry_create_project = insert ( ProjectsTable ).values (
					ProjectsTable.name_project == name , ProjectsTable.information == description ,
					ProjectsTable.limit_task == limit_task , ProjectsTable.status_project == status_project ,
					)
			
			
			
			except exc.SQLAlchemyError :
				print ( exc )
			result = await session.execute ( querry_create_project )
			return result
	
	@classmethod
	async def getProject ( cls , jwt_token: str ) -> ProjectsTable :
		async with async_session_maker ( ) as session :
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			guerry_get_project = (
				select ( ProjectsTable ).join ( UserToProject ).join (
					ProjectsTable.id_project == UserToProject.id_project
					).filter ( UserToProject.id_user == user_id )
			)
			
			result = await session.execute ( guerry_get_project )
			return result
		
		async def updateProject (
				cls , id_project: int , name: str , description: str , jwt_token: str
				) -> ProjectsTable :
			async with async_session_maker ( ) as session :
				payload = await cls.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				role = payload.get ( "role" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				if role != "admin" or role != "manager" :
					raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на создание проекта" )
				querry_update_project = (update(ProjectsTable ).values (ProjectsTable.name_project == name , ProjectsTable.information == description))
				result = await session.execute ( querry_update_project )
				return result
		
		@classmethod
		async def deleteProject ( cls , id_project: int , jwt_token: str ) :
			async with async_session_maker ( ) as session :
				payload = await cls.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				role = payload.get ( "role" )
				if role != "admin" or role != "manager" :
					raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на удаление проекта" )
				querry_delete_project = (
					delete(ProjectsTable, UserToProject ).join ( UserToProject ).join (project = id_project)
				)
				result = await session.execute ( querry_delete_project )
				return result
			
		
		@classmethod
		async def addUserProject ( cls , jwt_token: str , id_project: int , id_user_Added: int ) :
			async with async_session_maker ( ) as session :
				
				payload = await cls.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				role = payload.get ( "role" )
				if role != "admin" or role != "manager" :
					raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на создание проекта" )
				querry_add_user_project = insert ( UserToProject ).values (
					UserToProject.id_user == id_user_Added , UserToProject.project_id == id_project
					)
				result = await session.execute ( querry_add_user_project )
				return result
		
		@classmethod
		async def deleteUserProject ( cls , jwt_token: str , id_project: int , id_user_Added: int ) :
			async with async_session_maker ( ) as session :
				
				payload = await cls.decode_jwt_token ( jwt_token )
				user_id = payload.get ( "user_id" )
				if not user_id :
					raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
				role = payload.get ( "role" )
				if role != "admin" or role != "manager" :
					raise HTTPException ( status_code = 401 , detail = "Отсутствуют права на создание проекта" )
				querry_add_user_project = delete ( UserToProject ).filter (
					UserToProject.id_user == id_user_Added , UserToProject.project_id == id_project
					)
				result = await session.execute ( querry_add_user_project )
				return result
