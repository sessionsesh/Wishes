from django.urls import path
from . import views

app_name='authorization'

urlpatterns = [path('', views.home_view, name ="home"),
			   path('register', views.register_view, name='register'),
			   path('login', views.login_view, name='login'),
			   path('logout', views.logout_view, name='logout'),
			   path('profile/', views.user_profile_view, name="user_profile"),
			   path('profile/<int:ID>', views.profile_view, name="profile")]