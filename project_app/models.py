from django.db import models


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
