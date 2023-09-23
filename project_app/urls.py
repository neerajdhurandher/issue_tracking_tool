from django.urls import path
from .project.views_project import Project, ProjectByID
from .sprint.views_sprint import Sprint, SprintById
from .issue.views_issue import Issue
from .issue.views_watcher import Watcher

urlpatterns = [
    path("projects", Project.as_view(), name="Projects"),
    path("project/<str:project_id>", ProjectByID.as_view(), name="Project by ID"),
    path("sprints", Sprint.as_view(), name="Sprints"),
    path("sprint/<str:sprint_id>", SprintById.as_view(), name="Sprints"),
    path("issues", Issue.as_view(), name = "Issue"),
    path("issue/<str:issue_id>", Issue.as_view(), name = "Update Issue status"),
]
