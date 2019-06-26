FROM python:3.6
ADD ./requirements.txt /requirements.txt

RUN pip install pip --upgrade  && pip install  -r /requirements.txt -i  https://pypi.doubanio.com/simple/

ADD . /app
WORKDIR /app

CMD ["python" ,"docker-entrypoint.py" ]
