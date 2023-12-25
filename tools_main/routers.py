from tools_main.website.website_handlers import (
    add_website_handler,
    delete_website_handler,
    get_website_list_handler,
    update_website_handler,
)


def init_routes(app):
    # 网站管理
    app.add_api_route('/website',
                      get_website_list_handler, methods=['GET'])  # 获取网站列表
    app.add_api_route('/website',
                      add_website_handler, methods=['POST'])  # 添加网站
    app.add_api_route('/website/{site_id}',
                      update_website_handler, methods=['PUT'])  # 更新网站信息
    app.add_api_route('/website/{site_id}',
                      delete_website_handler, methods=['DELETE'])  # 删除网站

    # 标签管理
