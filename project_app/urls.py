from django.urls import path
from .project.views_project import ProjectView, ProjectByIDView
from .project.views_user_project_relation import UserProjectRelationView, UserProjectRelationByIDView
from .sprint.views_sprint import SprintView, SprintByIdView
from .issue.views_issue import IssueView
from .issue.views_watcher import WatcherView
from .comment.views_comment import CommentView
from .label.views_label import LabelView

urlpatterns = [
    path("projects", ProjectView.as_view(), name="Projects"),
    path("project/<str:project_id>", ProjectByIDView.as_view(), name="Project by ID"),
    path("userprojectrelation", UserProjectRelationView.as_view(),
         name="Create user project relation"),
    path("userprojectrelation/<str:project_id>", UserProjectRelationByIDView.as_view(),
         name="get all user of a project view"),
    path("userprojectrelation/<str:userprojectrelation_id>", UserProjectRelationView.as_view(),
         name="delete user_project_relation view"),
    path("sprints", SprintView.as_view(), name="Sprints"),
    path("sprint/<str:sprint_id>", SprintByIdView.as_view(), name="Sprints"),
    path("issues", IssueView.as_view(), name="Issue"),
    path("issue/<str:issue_id>", IssueView.as_view(), name="Update Issue status"),
    path("watchers", WatcherView.as_view(), name="Watcher"),
    path("watchers/<str:watcher_id>", WatcherView.as_view(), name="watcher by id"),
    path("comments", CommentView.as_view(), name="Comment"),
    path("comment/<str:comment_id>", CommentView.as_view(), name="comment by id"),
    path("labels", LabelView.as_view(), name="Label"),
    path("label/<str:label_id>", LabelView.as_view(), name="label by id"),

]
