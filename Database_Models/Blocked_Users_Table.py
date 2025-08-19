from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey

from database import Base


class BlockedUsersTable ( Base ) :
	__tablename__ = "blocked_users"
	id_block = Column ( Integer , primary_key = True )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	blocked_at = Column ( DateTime , nullable = False , default = datetime.now )
	unblock_at = Column ( DateTime , nullable = False , default = datetime.now )
	reason = Column ( String , nullable = False , default = None )

# CREATE TABLE blocked_users (
#     id_block INTEGER PRIMARY KEY,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     blocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     unblock_at TIMESTAMP NOT NULL,
#     reason TEXT
# );
