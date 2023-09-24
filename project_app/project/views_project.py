from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .project_serializer import ProjectSerializer
from ..utils import Utils
from ..models import Project as ProjectModel

import logging
logger = logging.getLogger(__name__)


class ProjectView(APIView):
    def post(self, request):
        """This API is to create a project
        Args:
            request : The request object contain project details
        """
        project_details = request.data

        if project_details['name'] is None or "":
            return Response({'name': ["This field may not be blank."]}, status=status.HTTP_400_BAD_REQUEST)

        valid_date_form = Utils.validate_datetime_format(
            project_details['start_date'])

        if valid_date_form == False:
            return Response({'start_date': f"Datetime has wrong format. Use one of these 	formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]. your data is {project_details['start_date']}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProjectSerializer(data=project_details)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """This API is to get all projects
        Args:
            request : None
        """
        all_projects = ProjectModel.objects.all()
        return Response(all_projects.values(), status=status.HTTP_200_OK)


class ProjectByIDView(APIView):
    def get(self, request, project_id):
        """This API is to get projects of given project_id
        Args:
            request : None
            project_id (str): Project id
        """
        logger.info(f"project id {project_id}")
        try:
            project = ProjectModel.objects.get(id=project_id)
            project_data = project.__dict__
            del project_data['_state']
            return Response(project_data, status=status.HTTP_200_OK)
        except ProjectModel.DoesNotExist:
            return Response({"error": "The project does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        """This API is to delete projects of given project_id
        Args:
            request : None
            project_id (str): Project id
        """
        logger.info(f"project id {project_id}")
        try:
            project = ProjectModel.objects.get(id=project_id)
            project.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except ProjectModel.DoesNotExist:
            return Response({"error": "The project does not exist"}, status=status.HTTP_404_NOT_FOUND)
