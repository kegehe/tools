FROM python:3.7.8

COPY . /app

WORKDIR ./app

RUN pip install fastapi[all] -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000

CMD python main/main.py