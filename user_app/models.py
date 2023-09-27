from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Cast, Substr, Length

# Create your models here.


class User(AbstractUser):
    id = models.CharField(max_length=100,
                          unique=True, editable=False, primary_key=True)
    organization_name = models.CharField(max_length=255,null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_user_id = get_model_id(self.__class__, 2)

            if last_user_id:
                self.id = f'user_id_{last_user_id + 1}'
            else:
                self.id = 'user_id_1'
        return super().save(*args, **kwargs)


def get_model_id(Model, split_after):
        data_1 = Model.objects.order_by(
            '-id').values_list('id', flat=True)
        data_2 = Model.objects.annotate(
            numeric_id=Cast(Substr('id', Length('id') - 1),
                            output_field=models.IntegerField())
        ).order_by('-numeric_id').values_list('id', flat=True)

        if len(data_1) > 9:
            last_id = data_2.first()
        else:
            last_id = data_1.first()

        if last_id:
            last_id = int(
                last_id.split('_')[split_after])
            return last_id
        return None
