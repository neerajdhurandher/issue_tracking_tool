import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core import serializers
from .project.project_serializer import ProjectSerializer
from .project.project_utils import ProjectUtils
from .models import Project as Project_Model

import logging
logger = logging.getLogger(__name__)


class Project(APIView):
    def post(self, request):
        """This API is to create a project
        Args:
            request : The request object contain project details
        """
        project_details = request.data

        if project_details['name'] is None or "":
            return Response({'name': ["This field may not be blank."]}, status=status.HTTP_400_BAD_REQUEST)

        valid_date_form = ProjectUtils.validate_datetime_format(
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
        all_projects = ProjectUtils.get_all_projects()
        return Response(all_projects, status=status.HTTP_200_OK)

    def get(self, request, project_id):
        """This API is to get projects of given project_id
        Args:
            request : None
            project_id (str): Project id
        """
        logger.info(f"project id {project_id}")
        try:
            project = Project_Model.objects.get(id=project_id)
            project_data = project.__dict__
            del project_data['_state']
            return Response(project_data, status=status.HTTP_200_OK)
        except Project_Model.DoesNotExist:
            return Response({"error": "The project does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, project_id):
        """This API is to delete projects of given project_id
        Args:
            request : None
            project_id (str): Project id
        """
        logger.info(f"project id {project_id}")
        try:
            project = Project_Model.objects.get(id=project_id)
            project.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except Project_Model.DoesNotExist:
            return Response({"error": "The project does not exist"}, status=status.HTTP_404_NOT_FOUND)
