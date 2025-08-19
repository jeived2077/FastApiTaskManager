from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , CheckConstraint
from sqlalchemy.dialects.postgresql import BYTEA

from database import Base


class User ( Base ) :
	__tablename__ = "users"
	id_user = Column ( Integer , primary_key = True )
	login = Column ( String ( 30 ) , nullable = False )
	password_hash = Column ( String ( 255 ) , nullable = False )
	email = Column ( String ( 254 ) , nullable = False , )
	role = Column ( String ( 20 ) , nullable = False , default = "member" , )
	photo= Column ( BYTEA )
	created_at = Column ( DateTime , nullable = False , default = datetime.now )
	CheckConstraint ( "email LIKE '%@%'" , name = "check_email_contains_at" )
	CheckConstraint ( "role IN ('admin', 'manager', 'member')" , name = "check_role_contains_at" )

# Запрос на создание таблицы в sql
# CREATE TABLE users (
#     id_user INTEGER PRIMARY KEY,
#     login VARCHAR(30) NOT NULL UNIQUE,
#     password_hash VARCHAR(255) NOT NULL,
#     email VARCHAR(254) NOT NULL UNIQUE CHECK(email Like "@"),
#     role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'manager', 'member')) DEFAULT 'member',
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
