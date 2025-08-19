from datetime import datetime

from sqlalchemy import Column , Integer , DateTime , INTEGER , ForeignKey
from sqlalchemy.dialects.postgresql import BYTEA , JSONB

from database import Base


class ReportProject ( Base ) :
	__tablename__ = "report_project"
	id_report_project = Column ( Integer , primary_key = True )
	id_project = Column ( INTEGER , ForeignKey ( "projects.id_project" , ondelete = "CASCADE" ) , nullable = False )
	created_at = Column ( DateTime , nullable = False , default = datetime.now )
	report_data = Column ( JSONB , nullable = True )
	files_project = Column ( BYTEA , nullable = True )

# CREATE TABLE report_project (
#     id_report_project INTEGER PRIMARY KEY,
#     id_project INTEGER NOT NULL REFERENCES projects(id_project) ON DELETE CASCADE,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     report_data JSONB, -- Для хранения данных отчета (например, burndown chart в формате JSON)
#     files_project BYTEA -- Вложения к отчету, если требуется
# );
