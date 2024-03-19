from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.api.v1.views.auth import register_user, login_user


urlpatterns = [
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
