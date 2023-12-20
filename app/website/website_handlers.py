from app.tools.db_mysql import fetchone


async def get_user_list_handler():
    sql = 'SELECT * FROM users;'
    res = await fetchone(sql)
    return res
