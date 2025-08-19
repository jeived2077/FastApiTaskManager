from sqlalchemy import Column , Integer , String

from database import Base


class PriorityTasksTable ( Base ) :
	__tablename__ = "priority_tasks"
	id_priority = Column ( Integer , primary_key = True )
	information_priority = Column ( String ( 100 ) , nullable = False )

# CREATE TABLE priority_tasks (
#     id_priority INTEGER PRIMARY KEY,
#     information_priority VARCHAR(100) NOT NULL
# );
