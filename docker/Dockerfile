FROM python:3.7.8

COPY . /app

WORKDIR ./app

RUN pip install -r ./requirements/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000

CMD python tools_main/app.py