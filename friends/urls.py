from django.urls import path
from . import views

app_name='friends'

urlpatterns = [path('friends/', views.friends_view, name ="friends"),
               path('explore', views.explore_view, name="explore"),
               path('ajax/explore_users/<str:regexp>', views.explore_users, name="explore_users"),
               path('ajax/explore_users/', views.explore_users_empty, name="explore_users_empty"),   # for empty search request
               path('friends/send_request/<int:ID>', views.send_friend_request, name="send_friend_request"),
               path('friends/accept_request/<int:ID>', views.accept_friend_request, name="accept_friend_request"),
               path('friends/dissolve/<int:ID>',views.dissolve_relationship, name="dissolve"),]
