import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello")
async def func1():
    return {'status': 1, 'msg': '请求成功', 'data': 'jenkins'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
