from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    organization_name = models.CharField(max_length=255,null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_user_id = self.__class__.objects.order_by(
                '-id').values_list('id', flat=True).first()
            if last_user_id:
                last_user_id = int(
                    last_user_id.split('_')[2])
                self.id = f'user_id_{last_user_id + 1}'
            else:
                self.id = 'user_id_1'
        return super().save(*args, **kwargs)
