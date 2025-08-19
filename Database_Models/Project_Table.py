from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey

from database import Base


class ProjectsTable ( Base ) :
	__tablename__ = "projects"
	id_project = Column ( Integer , primary_key = True )
	name_project = Column ( String ( 254 ) , nullable = False )
	information = Column ( INTEGER , ForeignKey ( "information_status.id_information" ) , nullable = True )
	status_project = Column ( String ( 256 ) , nullable = True )
	limit_task = Column ( INTEGER , nullable = True )
	created_at = Column ( DateTime , nullable = False , default = datetime.now )

# CREATE TABLE projects (
#     id_project INTEGER PRIMARY KEY,
#     name_project VARCHAR(254) NOT NULL,
#     information TEXT NOT NULL,
#     status_project INTEGER REFERENCES information_status(id_information),
#     limit_task INTEGER,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
