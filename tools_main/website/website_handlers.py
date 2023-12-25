from tools_main.models.website_models import Website
from tools_main.tools.db_mysql import execute, fetchmany_total


async def get_website_list_handler(page: int = 0, limit: int = 20):
    """
    获取网站列表
    """
    sql = 'SELECT * FROM `website` LIMIT %s, %s;'
    website_rs = await fetchmany_total(sql, args=(page, limit))

    return {'code': 200, 'msg': '添加成功', 'data': website_rs}


async def add_website_handler(website: Website):
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


async def update_website_handler(website: Website, site_id: int):
    """
    更新网站信息
    """
    sql = ('UPDATE `website` SET name = %s, url = %s, description = %s, keywords = %s, icon = %s, '
           'site_type = %s WHERE id = %s;')
    await execute(sql, args=(website.name, website.url, website.description, website.keywords,
                             website.icon, website.site_type, site_id))

    return {'code': 201, 'msg': '修改成功', 'data': {}}


async def delete_website_handler(site_id: int):
    """
    删除网站
    """
    sql = 'UPDATE `website` SET is_delete = 1 WHERE site_id = %s;'
    await execute(sql, args=(site_id,))

    return {'code': 204, 'msg': '添加成功', 'data': {}}
