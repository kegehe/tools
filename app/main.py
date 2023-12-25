import uvicorn
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.website.website_handlers import (
    add_website_handler,
    delete_website_handler,
    get_website_list_handler,
    update_website_handler,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=8000, reload=True)
