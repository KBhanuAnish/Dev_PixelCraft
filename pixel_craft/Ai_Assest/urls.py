from django.urls import path
from . import views
from .views import Chat_bot
urlpatterns = [
    path('',Chat_bot,name='chat_bot'),
]