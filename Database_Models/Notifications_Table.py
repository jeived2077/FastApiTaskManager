from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey

from database import Base

class NotificationTable ( Base ) :
	__tablename__ = "notifications"
	
	id_notification = Column ( Integer , primary_key = True )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	id_task = Column ( INTEGER , ForeignKey ( "tasks.id_task" , ondelete = "CASCADE" ) , nullable = False )
	id_project = Column ( INTEGER , ForeignKey ( "projects.id_project" , ondelete = "CASCADE" ) , nullable = False )
	notification_type = Column ( String ( 50 ) , nullable = False )
	message = Column ( String , nullable = False )
	created_at = Column ( DateTime , nullable = False , default = datetime.now )

# CREATE TABLE notifications (
#     id_notification INTEGER PRIMARY KEY,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     id_task INTEGER REFERENCES tasks(id_task) ON DELETE CASCADE,
#     id_project INTEGER REFERENCES projects(id_project) ON DELETE CASCADE,
#     notification_type VARCHAR(50) NOT NULL,
#     message TEXT NOT NULL,
#     is_read BOOLEAN DEFAULT FALSE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
