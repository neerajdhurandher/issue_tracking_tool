from django.db import models
from django.db.models import ForeignKey
from user_app.models import User, get_model_id


class BaseModel(models.Model):
    """
    Base model for all Model with common fields
    """

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class Project(models.Model):
    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    start_date = models.DateTimeField(default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    project_owner = models.CharField(max_length=100, null=True, default=None)

    def save(self, *args, **kwargs):
        if not self.id:
            last_project_id = get_model_id(self.__class__, 2)
            if last_project_id:
                self.id = f'project_id_{last_project_id + 1}'
            else:
                self.id = 'project_id_1'
        return super().save(*args, **kwargs)


class UserProjectRelation(BaseModel):
    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    user = ForeignKey(User, on_delete=models.CASCADE, null=False)
    project = ForeignKey(Project, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(null=False, default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_user_project_relation_id = get_model_id(self.__class__, 4)
            if last_user_project_relation_id:
                self.id = f'user_project_relation_id_{last_user_project_relation_id + 1}'
            else:
                self.id = 'user_project_relation_id_1'
        return super().save(*args, **kwargs)


class Sprint(BaseModel):
    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    project = ForeignKey(Project, on_delete=models.CASCADE)
    label = models.CharField(max_length=32)
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None)

    def save(self, *args, **kwargs):
        if not self.id:
            last_sprint_id = get_model_id(self.__class__, 2)
            if last_sprint_id:
                self.id = f'sprint_id_{last_sprint_id + 1}'
            else:
                self.id = 'sprint_id_1'
        return super().save(*args, **kwargs)


class Issue(BaseModel):
    issue_status_choice = [("O", "open"), ("C", "close")]
    issue_type_choice = [("B", "bug"), ("T", "type")]

    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=50)
    sprint = ForeignKey(Sprint, on_delete=models.SET_NULL, null=True)
    assignee = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=20, null=False,
                            choices=issue_type_choice)
    status = models.CharField(
        max_length=20, null=False, choices=issue_status_choice)

    def save(self, *args, **kwargs):
        if not self.id:
            last_issue_id = get_model_id(self.__class__, 2)
            if last_issue_id:
                self.id = f'issue_id_{last_issue_id + 1}'
            else:
                self.id = 'issue_id_1'
        return super().save(*args, **kwargs)


class Watcher(BaseModel):

    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    issue = ForeignKey(Issue, on_delete=models.CASCADE, null=False)
    user = ForeignKey(User, on_delete=models.CASCADE, null=False)
    is_active = models.BooleanField(null=False, default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_watcher_id = get_model_id(self.__class__, 2)
            if last_watcher_id:
                self.id = f'watcher_id_{last_watcher_id + 1}'
            else:
                self.id = 'watcher_id_1'
        return super().save(*args, **kwargs)


class Comment(BaseModel):

    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    issue = ForeignKey(Issue, on_delete=models.CASCADE, null=False)
    user = ForeignKey(User, on_delete=models.SET_DEFAULT,
                      null=False, default="Unknown user")
    comment = models.TextField(null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            last_comment_id = get_model_id(self.__class__, 2)
            if last_comment_id:
                self.id = f'comment_id_{last_comment_id + 1}'
            else:
                self.id = 'comment_id_1'
        return super().save(*args, **kwargs)


class Label(BaseModel):

    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    issue = ForeignKey(Issue, on_delete=models.CASCADE, null=False)
    label = models.CharField(max_length=200, null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            last_label_id = get_model_id(self.__class__, 2)
            if last_label_id:
                self.id = f'label_id_{last_label_id + 1}'
            else:
                self.id = 'label_id_1'
        return super().save(*args, **kwargs)
