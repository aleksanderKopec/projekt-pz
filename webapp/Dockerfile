FROM python:3
ENV DJANGO_SITE_ADRESS=http://achatapp.westeurope.cloudapp.azure.com
ENV DJANGO_DEBUG=False
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY docker/nginx.default /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/pip_cache
RUN mkdir -p /opt/app/chat
RUN mkdir -p /opt/app/chatapp
RUN mkdir -p /opt/app/static
RUN mkdir -p /opt/app/templates
COPY requirements.txt docker/start-server.sh /opt/app/
COPY chat /opt/app/chat/
COPY chatapp /opt/app/chatapp
COPY static /opt/app/static
COPY templates /opt/app/templates
WORKDIR /opt/app
RUN chmod 755 start-server.sh
RUN pip install -r requirements.txt
RUN chown -R www-data:www-data /opt/app
STOPSIGNAL SIGTERM
CMD ["/opt/app/start-server.sh"]