# Django chat webapp working with websocket
To run use: `python -m pip install -r requirements.txt` and `python manage.py runserver`
<br>
## To run as docker image: <br>
Build: `cd .../webapp & docker build -t django-chat-app .`<br>
Run: `docker run -it -p 8020:8020 django-chat-app`
## Environment variables
Enviroment variables used to control the application:
<ol>
    <li>DJANGO_DEBUG - controls whether django should 
        run in debug mode or production mode
        <ul> 
            <li>possible values: True/False</li>
            <li>default: False</li>
        </ul>
    </li>
    <li>DJANGO_SITE_ADRESS - the addres of site which django will be   
        hosted on
        <ul>
            <li> possible values: string, should be valid url</li>
            <li> default: http://achatapp.westeurope.cloudapp.azure.com</li>
    </li>
</ol>
    
