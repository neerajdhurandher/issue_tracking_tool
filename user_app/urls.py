from django.urls import path
from .views import UserView, GetAllUserView

urlpatterns = [
    path("user", GetAllUserView.as_view(), name="Get all User actions"),
    path("user/<str:user_id>", UserView.as_view(), name="User actions"),
    path("login", UserView.as_view(), name="login user"),
]
