from sqlalchemy import Column , Integer , String

from database import Base


class EntityTypesTable ( Base ) :
	__tablename__ = "entity_types"
	id_type = Column ( Integer , primary_key = True )
	name_type = Column ( String , nullable = False , default = None )

# CREATE TABLE entity_types (
#     id_type INTEGER PRIMARY KEY,
#     name_type VARCHAR(50) NOT NULL UNIQUE
# );
