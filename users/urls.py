from django.urls import path
from users.views import register, login_user, logout_user, activate_account,deposit

urlpatterns = [
    path("register/", register, name="register"),
    path("login_page/", login_user, name="login-page"),
    path("logout-user/", logout_user, name="logout-user"),
    path("activate/<int:user_id>/<str:token>/", activate_account),
    path('deposit/', deposit, name='deposit'),
]

