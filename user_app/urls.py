from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LoginUser, GetAllUsers

urlpatterns = [
       path("login", LoginUser.as_view(), name="login user"),
       path("get-all-users", GetAllUsers.as_view(), name="get all user"),

]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
