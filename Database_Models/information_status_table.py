from sqlalchemy import Column , Integer , String

from database import Base


class InformationStatusTable ( Base ) :
	__tablename__ = "information_status"
	id_information = Column ( Integer , primary_key = True )
	information_text_status = Column ( String ( 256 ) , nullable = False )

# CREATE TABLE information_status (
#     id_information INTEGER PRIMARY KEY,
#     information_text_status VARCHAR(256) NOT NULL
# );
