from sqlalchemy import Column , Integer , ForeignKey

from database import Base


class UserToProject ( Base ) :
	__tablename__ = "user_to_projects"
	id_user_to_project = Column ( Integer , primary_key = True )
	id_user = Column ( Integer , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False , )
	id_project = Column ( Integer , ForeignKey ( "projects.id_project" , ondelete = "CASCADE" ) , nullable = False )
	role_in_project = Column (
		Integer , ForeignKey ( "role_in_project.Idrole_in_project" , ondelete = "CASCADE" ) , nullable = False
		)

# CREATE TABLE user_to_project (
#     id_user_to_project INTEGER PRIMARY KEY,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     id_project INTEGER NOT NULL REFERENCES projects(id_project) ON DELETE CASCADE,
#     role_in_project INTEGER REFERENCES role_in_project(Idrole_in_project),
# );
