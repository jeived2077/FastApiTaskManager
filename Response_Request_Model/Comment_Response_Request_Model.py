
import datetime
from typing import Optional , List

from pydantic import BaseModel


class ResponseNestedCommentsModel ( BaseModel ) :
	id_comment: int
	text_comment: str
	created_At: datetime.datetime
	created_By: str
	loginUsername: str
	photo: bytes


class ResponseCommentsModel ( BaseModel ) :
	id_comment: int
	text_comment: str
	created_At: datetime.datetime
	created_By: str
	loginUsername: str
	photo: bytes
	nested_comments: List [ ResponseNestedCommentsModel ]
	
class RequestChangeComments ( BaseModel ) :
	comments_id: int
	text: Optional [ str ]
	photo_comments: Optional[bytes]
	
class RequestAddComments ( BaseModel ) :
	change_text: Optional [ str ]
	photo_comments: Optional [ bytes ]

class RequestDeleteComment ( BaseModel ) :
	id_commit: str