FROM python:3.10

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY . . 

ENTRYPOINT python3 websockets-test.py
