from sqlalchemy import select , insert , delete , update

from Database_Models import Detail_Commets_Table as Comments_Detail
from fastapi import HTTPException
from Database_Models.Comments_Table import CommentsTable
from Database_Models.User_Table import User
from database import async_session_maker


class CommentsDAO :
	model = CommentsTable
	
	@classmethod
	async def list_commets ( cls ) :
		async with async_session_maker ( ) as session :
			query = select (
				CommentsTable.datetime_create ,
				CommentsTable.is_edited ,
				User.login ,
				User.photo ,
				CommentsTable.id_comment ,
				CommentsTable.id_user ,
				CommentsTable.text_comment
				).join ( User , User.id_user == CommentsTable.id_user )
			result = await session.execute ( query )
			print ( "Запрос выполненин" )
			return result.scalars ( ).all ( )
	
	@classmethod
	async def add_commets ( cls, jwt_token: str, comment : str ) :
		async with async_session_maker ( ) as session :
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			query = (
				insert ( CommentsTable )
				.values ( User.id == user_id , CommentsTable.text_comment == comment )
			)
			result = await session.execute ( query )
			return result.scalars ( ).all ( )
	
	@classmethod
	async def delete_commets ( cls , id_comment: str, jwt_token: str ) :
		async with async_session_maker ( ) as session :
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			query = (delete ( CommentsTable ).filter ( CommentsTable.id_comment == id_comment ))
			result = await session.execute ( query )
			return result.scalars ( ).all ( )
	
	@classmethod
	async def update_commets ( cls , id_comment: str , text_comment: str, jwt_token: str ) :
		async with async_session_maker ( ) as session :
			payload = await cls.decode_jwt_token ( jwt_token )
			user_id = payload.get ( "user_id" )
			if not user_id :
				raise HTTPException ( status_code = 404 , detail = "Не найден пользователь" )
			query = (update ( CommentsTable.text_comment == text_comment , CommentsTable.is_edited == True ).filter (
				CommentsTable.id_comment == id_comment
				))
			result = await session.execute ( query )
			return result.scalars ( ).all ( )
	
	async def detail_comment ( self , id_comment: str ) :
		async with (async_session_maker ( ) as session) :
			query = (select (
				Comments_Detail.datetime_create , Comments_Detail.is_edited ,
				User.login , User.Photo , Comments_Detail.id_nestcomm , Comments_Detail.id_user ,
				Comments_Detail.text_comment
				).join (
				User , User.id == Comments_Detail.id_user
				).all ( ))
		result = await session.execute ( query )
		return result.scalars ( ).all ( )
