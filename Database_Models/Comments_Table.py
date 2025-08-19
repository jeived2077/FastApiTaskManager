from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey , BOOLEAN

from database import Base


class CommentsTable ( Base ) :
	__tablename__ = "comments"
	id_comment = Column ( Integer , primary_key = True )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	id_task  = Column ( Integer ,  ForeignKey ( "tasks.id_task" , ondelete = "CASCADE" ) , nullable = False )
	datetime_create = Column ( DateTime , nullable = False , default = datetime.now )
	text_comment = Column ( String , nullable = False , default = None )
	is_edited = Column ( BOOLEAN , nullable = False , default = False )
	

# CREATE TABLE comments (
#     id_comment INTEGER PRIMARY KEY,
#     id_task INTEGER NOT NULL REFERENCES tasks(id_task) ON DELETE CASCADE,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     text_comment TEXT NOT NULL,
#     datetime_create TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     is_edited BOOLEAN NOT NULL DEFAULT FALSE
# );
