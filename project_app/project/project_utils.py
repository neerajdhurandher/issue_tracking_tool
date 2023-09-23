from ..models import Project
from dateutil.parser import isoparse


class ProjectUtils():

    def validate_datetime_format(date_string):
        try:
            isoparse(date_string)

            return True
        except ValueError:
            return False

    def get_all_projects():
        all_projects = Project.objects.all()
        return all_projects.values()
