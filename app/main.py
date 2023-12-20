import uvicorn
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware  # 解决跨域问题

from app.website.website_handlers import get_user_list_handler

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_api_route('/user_list', get_user_list_handler, methods=['GET'])  # 添加网站

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
