import math
import re
from typing import Dict
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from tools_main.models.website_models import Website
from tools_main.tools.db_mysql import execute, fetchmany_total


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

    return {'code': 200, 'msg': '获取成功', 'data': data}


async def add_website_handler(website: Website) -> Dict:
    """
    添加网站
    """
    sql = ('INSERT INTO `website` (name, url, description, keywords, icon, site_type) '
           'VALUES (%s, %s, %s, %s, %s, %s)')
    website_id = await execute(sql, args=(website.name, website.url, website.description,
                                          website.keywords, website.icon, website.site_type))
    if not website_id:
        return {'code': 400, 'msg': '添加失败', 'data': {}}

    return {'code': 201, 'msg': '添加成功', 'data': {}}


async def add_website_by_url_handler(url: str) -> Dict:
    """
    通过链接添加网站
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 '
                      'Safari/537.36 '
                      'Edg/114.0.1823.58'
    }
    response = requests.get(url, headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取网站图标
    favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
    favicon_url = ''
    if favicon:
        favicon_url = favicon.get('href') or ''
        if 'https' not in favicon_url and 'http' not in favicon_url:
            favicon_url = f'https://{urlparse(url).netloc}{favicon_url}'

    # 获取网站描述
    description = soup.find('meta', attrs={'name': 'description'})
    description_content = description.get('content') if description else ''

    # 获取网站标题
    title = soup.title.string if soup.title else ''

    sql = ('INSERT INTO `website` (name, url, description, icon) '
           'VALUES (%s, %s, %s, %s, %s, %s)')
    website_id = await execute(sql, args=(title, url, description_content, favicon_url))
    if not website_id:
        return {'code': 400, 'msg': '添加失败', 'data': {}}

    return {'code': 201, 'msg': '添加成功', 'data': {}}


async def update_website_handler(website: Website, site_id: int) -> Dict:
    """
    更新网站信息
    """
    sql = ('UPDATE `website` SET name = %s, url = %s, description = %s, keywords = %s, icon = %s, '
           'site_type = %s WHERE id = %s;')
    await execute(sql, args=(website.name, website.url, website.description, website.keywords,
                             website.icon, website.site_type, site_id))

    return {'code': 201, 'msg': '修改成功', 'data': {}}


async def delete_website_handler(site_id: int) -> Dict:
    """
    删除网站
    """
    sql = 'UPDATE `website` SET is_delete = 1 WHERE site_id = %s;'
    await execute(sql, args=(site_id,))

    return {'code': 204, 'msg': '删除成功', 'data': {}}
