from database.requests import orm_get_id_private_users, orm_sub_day
from sqlalchemy.ext.asyncio import AsyncSession


def text_subscription(flag):
    return 'активна' if flag else 'неактивна'


def text_users(users):
    string = ''
    for user in users:
        string += f'• {user[1]} - {user[0]}\n'
    return string


async def remove_day_private(session: AsyncSession):
    users = await orm_get_id_private_users(session)
    for user in users:
        await orm_sub_day(session, user[0])