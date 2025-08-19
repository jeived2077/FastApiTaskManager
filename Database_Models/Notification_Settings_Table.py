from sqlalchemy import Column , Integer , String , ForeignKey , Boolean , CheckConstraint

from database import Base


class NotificationSettingsTable ( Base ) :
	__tablename__ = "notification_settings"
	
	id_setting = Column ( Integer , primary_key = True )
	id_user = Column ( Integer , ForeignKey ( "users.id_user" , ondelete = "CASCADE" ) , nullable = False )
	email_notifications = Column ( Boolean , default = True )
	websocket_notifications = Column ( Boolean , default = True )
	push_notifications = Column ( Boolean , default = False )
	notification_frequency = Column ( String ( 20 ) , nullable = False , default = "instant" )
	CheckConstraint ( "notification_frequency IN ('instant', 'daily', 'weekly')" , name = "check_notification_frequency_contains_at" )
	
	
	
	
	
# CREATE TABLE notification_settings (
#     id_setting INTEGER PRIMARY KEY,
#     id_user INTEGER NOT NULL REFERENCES users(id_user) ON DELETE CASCADE,
#     email_notifications BOOLEAN DEFAULT TRUE,
#     websocket_notifications BOOLEAN DEFAULT TRUE,
#     push_notifications BOOLEAN DEFAULT FALSE,
#     notification_frequency VARCHAR(20) CHECK (notification_frequency IN ('instant', 'daily', 'weekly')) DEFAULT
#     'instant'
# );
