from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , CheckConstraint , Text , TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey

from database import Base


class Tasks_Table ( Base ) :
    __tablename__ = "tasks"
    id_task = Column ( Integer , primary_key = True )
    id_project = Column ( Integer , ForeignKey('projects.id_project', ondelete = 'CASCADE'), nullable = False, )
    name = Column ( String ( 256 ) , nullable = False )
    description = Column ( Text , nullable = False , )
    priority = Column ( Integer , ForeignKey('priority_tasks.id_priority', ondelete = 'CASCADE'),  nullable = False, )
    status = Column ( Integer , ForeignKey('information_status.id_information', ondelete = 'CASCADE'), nullable = False,  )
    deadline= Column ( TIMESTAMP)
    created_at = Column ( TIMESTAMP , nullable = False , default=datetime.now )
    updated_at = Column ( TIMESTAMP, nullable = True , )

# CREATE TABLE tasks (
#     id_task INTEGER PRIMARY KEY,
#     id_project INTEGER NOT NULL REFERENCES projects(id_project) ON DELETE CASCADE,
#     name VARCHAR(256) NOT NULL,
#     description TEXT,
#     priority INTEGER REFERENCES priority_tasks(id_priority),
#     status INTEGER REFERENCES information_status(id_information), -- Ссылка на статус задачи
#     deadline TIMESTAMP,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP
# );
