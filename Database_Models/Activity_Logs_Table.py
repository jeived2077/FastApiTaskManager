from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey

from database import Base


class ActivityLogsTable ( Base ) :
	__tablename__ = "activity_logs"
	id_log = Column ( Integer , primary_key = True )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	action = Column ( String ( 256 ) , nullable = False )
	entity_type = Column ( INTEGER , ForeignKey ( "entity_types.id_type" , ondelete = "SET NULL" ) , nullable = False )
	role = Column ( String , nullable = False , default = "member" , )
	performed_at = Column ( DateTime , nullable = False , default = datetime.now )

# CREATE TABLE activity_logs (
#     id_log INTEGER PRIMARY KEY,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     action VARCHAR(256) NOT NULL,
#     entity_type INTEGER REFERENCES entity_types(id_type) ON DELETE SET NULL,
#     entity_id INTEGER,
#     performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
