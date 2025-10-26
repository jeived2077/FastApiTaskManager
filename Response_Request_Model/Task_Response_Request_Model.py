import datetime
from typing import Optional , List

from pydantic import BaseModel


class ResponseListProjectModel ( BaseModel ) :
	Id_Project: int
	Name_Project: str
	created_At: datetime.datetime
	created_By: str


class ResponseListPriorityModel ( BaseModel ) :
	name_priority: str


class ResponseListTaskModel ( BaseModel ) :
	Id_Task: int
	Name_Task: str
	created_At: datetime.datetime
	dealine_At: Optional [ datetime.datetime ]
	created_By: str
	name_priority: str


class ListFilter ( BaseModel ) :
	priority: Optional [ str ] = None
	filter: Optional [ str ] = None


class TasksAndProjectsResponse ( BaseModel ) :
	tasks: List [ ResponseListTaskModel ]
	projects: List [ ResponseListProjectModel ]
	priorities: List [ ResponseListPriorityModel ]




class StatusModelReponse ( BaseModel ) :
	id_status: int
	name_status: str


class TasksAndCommentsResponse ( BaseModel ) :
	Id_Task: int
	Name_Task: str
	created_At: datetime.datetime
	dealine_At: Optional [ datetime.datetime ]
	created_By: str
	name_priority: str
	status: List [ StatusModelReponse ]
