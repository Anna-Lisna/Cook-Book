from django.urls import path
from .views import *

urlpatterns = [
    path('register', register_attempt, name="register"),
    path('login', login_attempt, name="login"),
    path('logout', logout_attempt, name="logout"),
    path('token', token_send, name="token_send"),
    path('verify/<email_token>', verify, name="verify"),
    path('error', error_page, name="error"),
    path('profile', UserProfile.as_view(), name='user_profile'),
    path('edit', UserUpdate.as_view(), name='update_profile'),
]
