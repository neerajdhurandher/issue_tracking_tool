from django.urls import path
from .views import Project

urlpatterns = [
    path("projects", Project.as_view(), name="Projects"),
    path("projects/<str:project_id>", Project.as_view(), name="Delete Project")

]
