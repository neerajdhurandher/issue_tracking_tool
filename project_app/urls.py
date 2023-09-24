from django.urls import path
from .project.views_project import Project, ProjectByID
from .project.views_user_project_relation import UserProjectRelation
from .sprint.views_sprint import Sprint, SprintById
from .issue.views_issue import Issue
from .issue.views_watcher import Watcher

urlpatterns = [
    path("projects", Project.as_view(), name="Projects"),
    path("project/<str:project_id>", ProjectByID.as_view(), name="Project by ID"),
    path("userprojectrelation", UserProjectRelation.as_view(),
         name="Create user project relation"),
    path("userprojectrelation/<str:project_id>", UserProjectRelation.as_view(),
         name="get all user of a project view"),
    path("sprints", Sprint.as_view(), name="Sprints"),
    path("sprint/<str:sprint_id>", SprintById.as_view(), name="Sprints"),
    path("issues", Issue.as_view(), name="Issue"),
    path("issue/<str:issue_id>", Issue.as_view(), name="Update Issue status"),
    path("watchers", Watcher.as_view(), name="Create watcher"),

]
