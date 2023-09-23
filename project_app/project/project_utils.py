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

    def get_project_by_id(project_id):
        try:
            project = Project.objects.get(id=project_id)
            project_data = project.__dict__
            del project_data['_state']
            return ({'status': True, 'data': project_data})
        except Project.DoesNotExist:
            return ({'status': False, "error": "The project does not exist"})
