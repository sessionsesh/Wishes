from django.urls import path
from . import views

app_name='authorization'

urlpatterns = [path('register', views.register_view, name='register'),
			   path('login', views.login_view, name='login'),
			   path('logout', views.logout_view, name='logout'),
			   path('users', views.users_view, name="users"),]