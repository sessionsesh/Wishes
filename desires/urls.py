from django.urls import path
from . import views

app_name='desires'

urlpatterns = [path('desires', views.desires_view, name="desires"),
               path('desires/delete/<ID>', views.desire_delete, name="delete_desire"),
               path('desires/add', views.desire_add, name="add_desire")]
