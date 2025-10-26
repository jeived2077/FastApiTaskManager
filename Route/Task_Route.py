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


class ListFilter( ):
    priority: Optional[str] = None
    filter: Optional[str] = None


class TasksAndProjectsResponse(BaseModel):
    tasks: List[ResponseListTaskModel]
    projects: List[ResponseListProjectModel]
    priorities: List[ResponseListPriorityModel]


@router.get("/", summary="Вывести задачи и проекты", response_model=TasksAndProjectsResponse)
async def listtasksandproject(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    list_filter: ListFilter = Depends(ListFilter),
    
):
    jwt_token = credentials.credentials
    data = await TaskDao.gettasksandproject(
        jwt_token = jwt_token,
        priority=list_filter.priority,
        filter=list_filter.filter
    )
    return data


class ResponseNestedCommentsModel(BaseModel) :
    id_comment: int
    text_comment: str
    created_At: datetime.datetime
    created_By: str
    loginUsername: str
    photo: bytes


class ResponseCommentsModel(BaseModel):
    id_comment: int
    text_comment: str
    created_At: datetime.datetime
    created_By: str
    loginUsername: str
    photo: bytes
    nested_comments: List[ResponseNestedCommentsModel]
    





class TasksAndCommentsResponse(BaseModel):
    Id_Task: int
    Name_Task: str
    created_At: datetime.datetime
    dealine_At: Optional [ datetime.datetime ]
    created_By: str
    name_priority: str
    comments: List[ResponseCommentsModel]

@router.put("/changestatus{id_task}", summary = "Изменение статуса задачи")
async def changestatustask(
        id_task: int, id_status: int,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
         response_model= TasksAndCommentsResponse
        
        ):
    data = await TaskDao.change_status_task(
        jwt_token = credentials.credentials,
        id_task = id_task,
        status = id_status,
        )
    return data
    