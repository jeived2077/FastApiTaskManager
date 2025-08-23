import datetime
from typing import Optional, List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from DAO.Task_Dao import TaskDao

bearer_scheme = HTTPBearer()

router = APIRouter(prefix="/tasks", tags=["Задачи"])

class ResponseListProjectModel(BaseModel):
    Id_Project: int
    Name_Project: str
    created_At: datetime.datetime
    created_By: str

class ResponseListPriorityModel(BaseModel):
    name_priority: str

class ResponseListTaskModel(BaseModel):
    Id_Task: int
    Name_Task: str
    created_At: datetime.datetime
    dealine_At: Optional[datetime.datetime]
    created_By: str
    name_priority: str


class ListFilter():
    priority: Optional[str] = None
    filter: Optional[str] = None


class TasksAndProjectsResponse(BaseModel):
    tasks: List[ResponseListTaskModel]
    projects: List[ResponseListProjectModel]
    priorities: List[ResponseListPriorityModel]


@router.get("/", summary="Вывести задачи и проекты", response_model=TasksAndProjectsResponse)
async def listtasksandproject(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    list_filter: ListFilter = Depends(ListFilter)
):
    jwt_token = credentials.credentials
    data = await TaskDao.gettasksandproject(
        jwt_token,
        priority=list_filter.priority,
        filter=list_filter.filter
    )
    return data