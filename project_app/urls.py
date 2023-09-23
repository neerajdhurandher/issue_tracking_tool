from django.urls import path
from .project.views_project import Project, ProjectByID

urlpatterns = [
    path("projects", Project.as_view(), name="Projects"),
    path("project/<str:project_id>", ProjectByID.as_view(), name="Project by ID"),

]
