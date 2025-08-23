from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey

from database import Base


class ProjectsToUserTable ( Base ) :
	__tablename__ = "user_to_projects"
	id_user_to_projects = Column ( Integer , primary_key = True )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" ) , nullable = True )
	id_project = Column ( INTEGER , ForeignKey ( "projects.id_project" ) , nullable = True )
	status_project = Column ( String ( 256 ) , nullable = True )
	limit_task = Column ( INTEGER , nullable = True )
	added_at = Column ( DateTime , nullable = False , default = datetime.now )
