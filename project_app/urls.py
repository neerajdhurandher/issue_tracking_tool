from django.urls import path
from .project.views_project import ProjectView
from .user_project_relation.views_user_project_relation import UserProjectRelationView
from .sprint.views_sprint import SprintView
from .issue.views_issue import IssueView, MultipleQueryIssueList
from .watcher.views_watcher import WatcherView
from .comment.views_comment import CommentView
from .label.views_label import LabelView

urlpatterns = [
    path("projects", ProjectView.as_view(), name="Projects"),
    path("project/<str:project_id>",
         ProjectView.as_view(), name="Project by ID"),
    path("userprojectrelation", UserProjectRelationView.as_view(),
         name="Create user project relation"),
    path("userprojectrelation/<str:id>", UserProjectRelationView.as_view(),
         name="delete user_project_relation view"),

    path("sprints", SprintView.as_view(), name="Sprints"),
    path("sprint/<str:sprint_id>", SprintView.as_view(), name="Sprint ids"),
    path("issues", IssueView.as_view(), name="Issue"),
    path("issue/<str:issue_id>", IssueView.as_view(), name="Update Issue status"),
    path("search_issues", MultipleQueryIssueList.as_view(),
         name="Multiple query search Issue"),
    path("watchers", WatcherView.as_view(), name="Watcher"),
    path("watcher/<str:watcher_id>", WatcherView.as_view(), name="watcher by id"),
    path("comments", CommentView.as_view(), name="Comment"),
    path("comment/<str:comment_id>", CommentView.as_view(), name="comment by id"),
    path("labels", LabelView.as_view(), name="Label"),
    path("label/<str:label_id>", LabelView.as_view(), name="label by id"),

]
