from datetime import datetime

from sqlalchemy import Column , Integer , String , DateTime , INTEGER , ForeignKey , BOOLEAN

from database import Base


class CommentsTable ( Base ) :
	__tablename__ = "nested_comments"
	id_nestcomm = Column ( Integer , primary_key = True )
	id_commit = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	id_user = Column ( INTEGER , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	text_comment = Column ( String , nullable = False , default = None )
	datetime_create= Column ( DateTime , nullable = False , default = datetime.now )
	is_edited = Column ( BOOLEAN , nullable = False , default = False )
	
	
	
	
	
# CREATE TABLE public."nested_comments" (
# 	id_nestcomm int4 NOT NULL,
# 	id_commit int4 NOT NULL,
# 	id_user int4 NOT NULL,
# 	text_comment text NOT NULL,
# 	datetime_create timestamp DEFAULT CURRENT_TIMESTAMP NULL,
# 	is_edited bool DEFAULT false NOT NULL,
# 	CONSTRAINT nestcomm_pkey PRIMARY KEY (id_nestcomm),
# 	CONSTRAINT nestcomm_id_task_fkey FOREIGN KEY (id_commit) REFERENCES public."comments" (id_comment) ON DELETE CASCADE,
# 	CONSTRAINT nestcomm_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id_user) ON DELETE CASCADE
# );
