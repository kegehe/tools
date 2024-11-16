from typing import Dict

from tools_main.models.website_models import User
from tools_main.util.db_mysql import execute, fetchone


async def user_sign_in_handler(user: User) -> Dict:
    """
    用户注册
    """
    # 短信验证

    sql = 'SELECT id FROM user WHERE phone = %s LIMIT 1;'
    user_res = await fetchone(sql, args=(user.phone,))
    if user_res:
        return {'code': 400, 'msg': '请求失败, 电话已被注册', 'data': {}}

    sql = 'INSERT INTO user (name, logo_url, phone, password) VALUES (%s, %s, %s, %s);'
    user_id = await execute(sql, args=(user.name, user.logo_url, user.phone, user.password))
    if not user_id:
        return {'code': 400, 'msg': '请求失败, 用户注册失败', 'data': {}}

    return {}


async def user_login_handler(phone: str, password: str) -> Dict:
    """
    用户登录
    """
    sql = 'SELECT * FROM user WHERE phone = %s AND password = %s LIMIT 1;'
    user_res = await fetchone(sql, args=(phone, password))
    if not user_res:
        return {'code': 400, 'msg': '请求失败, 账户或密码错误', 'data': {}}
    elif user_res['status'] != 1:
        return {'code': 400, 'msg': '请求失败, 用户被禁用', 'data': {}}

    del user_res['password']

    return {'code': 200, 'msg': '请求成功', 'data': user_res}


async def delete_account_handler(phone: str, password: str) -> Dict:
    """
    用户注销
    """
    # 短信验证

    sql = 'SELECT id FROM user WHERE phone = %s AND password = %s LIMIT 1;'
    user_res = await fetchone(sql, args=(phone, password))
    if not user_res:
        return {'code': 400, 'msg': '请求失败, 用户不存在', 'data': {}}

    sql = 'DELETE FROM user WHERE id = %s;'
    await execute(sql, user_res['id'])

    return {}
