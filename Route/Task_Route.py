import datetime
from typing import Optional , List

from fastapi import APIRouter , Depends
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from pydantic import BaseModel

from DAO.Task_Dao import TaskDao
from Response_Request_Model.Task_Response_Request_Model import (
	ListFilter , TasksAndProjectsResponse ,
	TasksAndCommentsResponse ,
	)

bearer_scheme = HTTPBearer ( )

router = APIRouter ( prefix = "/tasks" , tags = [ "Задачи" ] )




@router.get ( "/" , summary = "Вывести задачи и проекты" , response_model = TasksAndProjectsResponse )
async def listtasksandproject (
		credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme ) ,
		list_filter: ListFilter = Depends ( ListFilter ) ,
		
		) :
	jwt_token = credentials.credentials
	data = await TaskDao.gettasksandproject (
		jwt_token = jwt_token ,
		priority = list_filter.priority ,
		filter = list_filter.filter
		)
	return data




@router.put ( "/changestatus/{id_task}" , summary = "Изменение статуса задачи" )
async def changestatustask (
		id_task: int , id_status: int ,
		credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme ) ,
		
		) :
	data = await TaskDao.change_status_task (
		jwt_token = credentials.credentials ,
		id_task = id_task ,
		status = id_status ,
		)
	return data


@router.get (
	"/detail/{id_task}" , summary = "Получить детальную информация задачи с комментариями" ,
	response_model = TasksAndCommentsResponse
	)
async def detail_task (
		id_task: int , credentials: HTTPAuthorizationCredentials = Depends ( bearer_scheme ) ,
		
		) :
	data = await TaskDao.task_detail_information (
		jwt_token = credentials.credentials ,
		id_task = id_task ,
		)
	return data
