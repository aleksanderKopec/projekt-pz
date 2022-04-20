FROM python

RUN apt-get update && apt-get install nginx vim -y --no-install-recommends

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY docker/nginx.default /etc/nginx/sites-available/default

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

RUN nginx -g "daemon off;"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]