from django.urls import path
from . import views

app_name='desires'

urlpatterns = [path('desires', views.desires_view, name="desires"),]
