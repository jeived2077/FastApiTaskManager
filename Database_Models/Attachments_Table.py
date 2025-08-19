from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA

from database import Base


class AttachmentsTable ( Base ) :
	__tablename__ = "attachments"
	id_attachment = Column ( Integer , primary_key = True )
	id_task = Column ( INTEGER , ForeignKey ( "tasks.id_task" , ondelete = "CASCADE" ) , nullable = False )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	file_name = Column ( String ( 256 ) , nullable = False )
	file_data = Column ( BYTEA , nullable = False )
	uploaded_at = Column ( DateTime , nullable = False , default = datetime.now )

# CREATE TABLE attachments (
#     id_attachment INTEGER PRIMARY KEY,
#     id_task INTEGER NOT NULL REFERENCES tasks(id_task) ON DELETE CASCADE,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     file_name VARCHAR(256) NOT NULL,
#     file_data BYTEA NOT NULL,
#     uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
