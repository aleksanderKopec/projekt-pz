from django.urls import path
from .views import Chat, ChatRoom

urlpatterns = [
    path('', Chat.as_view()),
    path('<str:chatroom>/', ChatRoom.as_view())
]