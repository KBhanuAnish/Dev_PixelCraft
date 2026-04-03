from django.urls import path
from . import views

urlpatterns = [
    path('', views.components_list, name='components_list'),
]