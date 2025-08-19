import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession
from sqlalchemy.orm import DeclarativeBase , sessionmaker

load_dotenv ( )

DB_USER = os.environ.get ( "DB_USER" , "postgres" )
DB_PASS = os.environ.get ( "DB_PASS" , "1234" )
DB_HOST = os.environ.get ( "DB_HOST" , "localhost" )
DB_PORT = os.environ.get ( "DB_PORT" , "5432" )
DB_NAME = os.environ.get ( "DB_NAME" , "Platform_database" )

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print ( f"DATABASE_URL: {DATABASE_URL}" )

async_engine = create_async_engine ( DATABASE_URL , echo = True )

async_session_maker = sessionmaker ( async_engine , expire_on_commit = False , class_ = AsyncSession )


class Base ( DeclarativeBase ) :
	pass
