import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from DAO.Task_Dao import TaskDao
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer_scheme = HTTPBearer()

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.get("/", summary="Вывести задачи")
async def listtask(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
  jwt_token = credentials.credentials
  return await TaskDao.getTasks(jwt_token)










#
#
#
# @router.post ( "/create" , summary="Добавить задачу")
# def createtask ( ) :
# 	pass
#
#
# @router.delete ( "/delete/{task_id}" , include_in_schema = False, summary="Удалить задачу" )
#
#
# def deletetask ( task_id: int ) :
# 	pass
#
#
# @router.patch ( "/change/{task_id}" , include_in_schema = False, summary="Изменить задачу" )
#
#
# def changetask ( task_id: int ) :
# 	pass
#
#
# @router.get ( "/detail/{task_id}" , include_in_schema = False, summary="Подробная задача" )
#
#
# def detailtask ( task_id: int ) :
# 	pass
