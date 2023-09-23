from django.db import models
from django.db.models import ForeignKey
from user_app.models import User


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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            last_project_id = self.__class__.objects.order_by(
                '-id').values_list('id', flat=True).first()
            if last_project_id:
                last_project_id = int(last_project_id.split('_')[2])
                self.id = f'project_id_{last_project_id + 1}'
            else:
                self.id = 'project_id_1'
        return super().save(*args, **kwargs)


class Sprint(BaseModel):
    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    project = ForeignKey(Project, on_delete=models.CASCADE)
    label = models.CharField(max_length=32)
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None)

    # def __str__(self):
    #     return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            last_sprint_id = self.__class__.objects.order_by(
                '-id').values_list('id', flat=True).first()
            if last_sprint_id:
                last_sprint_id = int(last_sprint_id.split('_')[2])
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

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            last_issue_id = self.__class__.objects.order_by(
                '-id').values_list('id', flat=True).first()
            if last_issue_id:
                last_issue_id = int(last_issue_id.split('_')[2])
                self.id = f'issue_id_{last_issue_id + 1}'
            else:
                self.id = 'issue_id_1'
        return super().save(*args, **kwargs)


class Watcher(BaseModel):

    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    issue = ForeignKey(Issue, on_delete=models.CASCADE, null=True)
    user = ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            last_issue_id = self.__class__.objects.order_by(
                '-id').values_list('id', flat=True).first()
            if last_issue_id:
                last_issue_id = int(last_issue_id.split('_')[2])
                self.id = f'issue_id_{last_issue_id + 1}'
            else:
                self.id = 'issue_id_1'
        return super().save(*args, **kwargs)
