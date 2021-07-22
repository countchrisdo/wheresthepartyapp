from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.events_index, name='index'),
    path('accounts/profile/', views.profile, name='profile'),
    
    path('events/<int:pk>/', views.EventDetail.as_view(), name='detail'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('events/<int:event_id>/add_rating/', views.add_rating, name='add_rating'),
    path('events/<int:event_id>/add_comment/', views.add_comment, name='add_comment'),
    path('events/<int:pk>/', views.CommentDetail.as_view(), name='comments_detail'),
    path('events/<int:event_id>/add_photo/', views.add_photo, name='add_photo'),

    path('comments/<int:pk>/delete/', views.CommentDelete.as_view(), name='delete_comment'),
    path('comments/<int:pk>/update/', views.CommentUpdate.as_view(), name='update_comment'),

    path('accounts/signup/', views.signup, name='signup'),
]
