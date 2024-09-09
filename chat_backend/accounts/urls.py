from django.urls import path 
from .views import (
    get_profiles_view,
    register_view, 
    update_profile_view,
    login_view,
    validate_username_email,
)

app_name = 'accounts'


urlpatterns = [
    path('users/', get_profiles_view, name='profiles'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('update/profile/', update_profile_view, name='update'),
    path('validate/', validate_username_email, name='validate-username-email'),
]
