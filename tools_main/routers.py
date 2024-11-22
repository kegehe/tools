from tools_main.api.website.handler.website_handlers import (
    add_website_by_url_handler,
    add_website_handler,
    delete_website_handler,
    get_website_info_by_url_handler,
    get_website_list_handler,
    update_website_handler,
)


def init_routes(app):

    # 网站管理
    app.add_api_route('/website', get_website_list_handler,
                      methods=['GET'])  # 获取网站列表
    app.add_api_route('/website', add_website_handler,
                      methods=['POST'])  # 添加网站
    app.add_api_route('/website/{site_id}', update_website_handler,
                      methods=['PUT'])  # 更新网站信息
    app.add_api_route('/website/{site_id}', delete_website_handler,
                      methods=['DELETE'])  # 删除网站
    app.add_api_route('/website/url', get_website_info_by_url_handler,
                      methods=['GET'])  # 通过链接获取网站信息
    app.add_api_route('/website/url', add_website_by_url_handler,
                      methods=['POST'])  # 通过链接添加网站
    # 账户管理

    # 标签管理

    # 操作记录

    # 操作日志管理

    # 后台管理
