from django.urls import path 
from .views import home_view

app_name = 'chat'


urlpatterns = [
    path('messages/', home_view, name='message'),
]
