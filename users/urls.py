from django.urls import path

from users.apps import UsersConfig
from users.views import UserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserLoginView.as_view(template_name='users/login.html'), name='login'),
]