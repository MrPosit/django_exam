from django.urls import path
from . import views
from forum.routing import websocket_urlpatterns
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.ThreadListView.as_view(), name='thread_list'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='logged_out.html', next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name='thread_detail'),
    path('thread/new/', views.ThreadCreateView.as_view(), name='thread_create'),
    path('thread/<int:pk>/reply/', views.MessageCreateView.as_view(), name='message_create'),
    path('like-thread/<int:thread_id>/', views.like_thread, name='like_thread'),
    path('like-message/<int:message_id>/', views.like_message, name='like_message'),
    path('search/', views.ThreadSearchView.as_view(), name='thread_search'), 
    path('create-thread/', views.create_thread, name='create_thread'),
] + websocket_urlpatterns
