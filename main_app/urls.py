from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('events/', views.events_index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('events/<int:event_id>/add_photo', views.add_photo, name='add_photo'),
]
