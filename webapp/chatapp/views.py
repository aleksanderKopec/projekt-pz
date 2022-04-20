from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

# Create your views here.


class Chat(View):
    def get(self, request: HttpRequest):
        return render(request, 'title_page.html')


class ChatRoom(View):
    def get(self, request: HttpRequest, chatroom: str):
        return render(request, 'room_page.html', {"room_name": chatroom})



