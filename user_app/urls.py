from django.urls import path
from .views import LoginUser, GetAllUsers, GetUserByID

urlpatterns = [
    path("login", LoginUser.as_view(), name="login user"),
    path("get-all-users", GetAllUsers.as_view(), name="get all user"),
    path("<int:user_id>", GetUserByID.as_view(), name="get user by id"),
]
