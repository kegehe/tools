import math
import re
from typing import Dict

from tools_main.models.website_models import Website
from tools_main.tools.db_mysql import execute, fetchmany_total
from tools_main.website.tools.website_tools import get_website_info


async def get_website_list_handler(search_key: str = '', page: int = 0, limit: int = 20) -> Dict:
    """
    获取网站列表
    """
    if page <= 0:
        page = 1
    if limit > 100:
        limit = 100
    start = (page - 1) * limit

    args_data = []
    search_sql = ''
    if search_key:
        search_sql = 'name REGEXP %s OR description REGEXP %s OR keywords REGEXP %s'
        args_data.extend([re.escape(search_key)] * 3)

    args_data.extend([start, limit])

    sql = f'SELECT * FROM `website` {search_sql} LIMIT %s, %s;'
    website_rs = await fetchmany_total(sql, args=args_data)

    all_page = math.ceil(website_rs['total'] / limit)
    data = {'count': website_rs['total'],
            'all_page': all_page,
            'now_page': page,
            'website_list': website_rs['data']}

    return {'code': 200, 'msg': '请求成功', 'data': data}


async def add_website_handler(website: Website) -> Dict:
    """
    添加网站
    """
    sql = ('INSERT INTO `website` (name, url, description, keywords, icon, site_type) '
           'VALUES (%s, %s, %s, %s, %s, %s)')
    website_id = await execute(sql, args=(website.name, website.url, website.description,
                                          website.keywords, website.icon, website.site_type))
    if not website_id:
        return {'code': 400, 'msg': '请求失败', 'data': {}}

    return {'code': 201, 'msg': '请求成功', 'data': {}}


async def get_website_info_by_url_handler(url: str) -> Dict:
    """
    通过链接获取网站信息
    """
    data = await get_website_info(url)

    return {'code': 201, 'msg': '请求成功', 'data': data}


async def add_website_by_url_handler(url: str) -> Dict:
    """
    通过链接添加网站
    """
    data = await get_website_info(url)

    sql = ('INSERT INTO `website` (name, url, description, icon) '
           'VALUES (%s, %s, %s, %s)')
    website_id = await execute(sql, args=(data['name'], data['url'], data['description'], data['icon']))
    if not website_id:
        return {'code': 400, 'msg': '请求失败', 'data': {}}

    return {'code': 201, 'msg': '请求成功', 'data': {}}


async def update_website_handler(website: Website, site_id: int) -> Dict:
    """
    更新网站信息
    """
    sql = ('UPDATE `website` SET name = %s, url = %s, description = %s, keywords = %s, icon = %s, '
           'site_type = %s WHERE id = %s;')
    await execute(sql, args=(website.name, website.url, website.description, website.keywords,
                             website.icon, website.site_type, site_id))

    return {'code': 201, 'msg': '请求成功', 'data': {}}


async def delete_website_handler(site_id: int) -> Dict:
    """
    删除网站
    """
    sql = 'UPDATE `website` SET is_delete = 1 WHERE site_id = %s;'
    await execute(sql, args=(site_id,))

    return {'code': 204, 'msg': '请求成功', 'data': {}}
