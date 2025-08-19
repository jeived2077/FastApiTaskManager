from sqlalchemy import Column , Integer , String

from database import Base


class RoleInProjectsTable ( Base ) :
	__tablename__ = "role_in_project"
	id_role_in_project = Column ( Integer , primary_key = True )
	TextRole = Column ( String ( 254 ) , nullable = False , default = "member" , )


# CREATE TABLE role_in_project(
# Idrole_in_project INTEGER PRIMARY KEY,
# TextRole VARCHAR(254) NOT NULL
# )