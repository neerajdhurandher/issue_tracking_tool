from ..models import Project
from dateutil.parser import isoparse
from ..models import UserProjectRelation
from django.db.models import Q


class ProjectUtils():

    def user_existence_in_project(user_obj, project_obj):
        try:
            data = UserProjectRelation.objects.filter(
                Q(project=project_obj) & Q(user=user_obj))
            if len(data) == 0:
                return False
            return True
        except Exception as error:
            return False

    def get_all_users_of_a_project(project_id):
        try:
            all_users = UserProjectRelation.objects.filter(project=project_id)
            return all_users
        except Exception as error:
            return None

    def get_user_status_in_project(user_id, project_id):
        try:
            data = UserProjectRelation.objects.filter(
                Q(project=project_id) & Q(user=user_id))
            if len(data) == 1:
                if data[0].is_active:
                    return True
            return False
        except Exception as error:
            return False
        