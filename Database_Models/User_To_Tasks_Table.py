from sqlalchemy import Column , Integer , ForeignKey

from database import Base


class UserToTasks ( Base ) :
	__tablename__ = "user_to_tasks"
	id_user_to_tasks = Column ( Integer , primary_key = True )
	id_task = Column ( Integer , ForeignKey ( "tasks.id_task" , ondelete = "CASCADE" ) , nullable = False )
	id_user = Column ( Integer , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	
	
# CREATE TABLE user_to_tasks (
#     id_user_to_tasks INTEGER PRIMARY KEY,
#     id_task INTEGER NOT NULL REFERENCES tasks(id_task) ON DELETE CASCADE,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE
# );
