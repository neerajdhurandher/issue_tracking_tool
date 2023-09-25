from django.urls import path
from .views import LoginUserView, GetAllUsersView, UserView

urlpatterns = [
    path("login", LoginUserView.as_view(), name="login user"),
    path("user", GetAllUsersView.as_view(), name="get all user"),
    path("user/<str:user_id>", UserView.as_view(), name="get user by id"),
]
