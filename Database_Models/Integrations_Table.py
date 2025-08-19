from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey

from database import Base


class IntegrationsTable ( Base ) :
	__tablename__ = "integrations"
	id_integration = Column ( Integer , primary_key = True )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	service_name = Column ( String(100) , nullable = False )
	access_token =  Column ( String , nullable = False , default = None )
	created_at =  Column ( DateTime , nullable = False , default = datetime.now )


# CREATE TABLE integrations (
#     id_integration INTEGER PRIMARY KEY,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     service_name VARCHAR(100) NOT NULL,
#     access_token TEXT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );