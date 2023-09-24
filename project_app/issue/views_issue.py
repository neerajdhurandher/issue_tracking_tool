from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from ..utils import Utils
from .issue_serializer import IssueSerializer
from ..models import Issue as IssueModel, Sprint as SprintModel, Project as ProjectModel
from ..constants import pagination_limit
import logging
logger = logging.getLogger(__name__)


class Issue(APIView):
    def post(self, request):
        issue_data = request.data

        if issue_data['title'] is None:
            return Response({"title": "This field may not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        sprint_id = issue_data['sprint']

        if sprint_id is None:
            return Response({"sprint": "This field may not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        sprint_exits = Utils.get_object_by_id(SprintModel, sprint_id)

        if sprint_exits['status'] == False:
            return Response(sprint_exits['error'].format(
                "sprint"), status=status.HTTP_404_NOT_FOUND)

        serializer = IssueSerializer(data=issue_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        page_no = request.GET.get('page')
        project_id = request.GET.get('project')

        if not page_no:
            return Response({"error": "Page param not passed"}, status=status.HTTP_400_BAD_REQUEST)

        if not project_id:
            return Response({"error": "Project/Assignee param is not passed"}, status=status.HTTP_400_BAD_REQUEST)

        project_exits = Utils.get_object_by_id(ProjectModel, project_id)
        if project_exits['status'] == False:
            return Response(project_exits['error'].format("project"), status=status.HTTP_404_NOT_FOUND)

        try:
            sprint = get_object_or_404(SprintModel, project_id=project_id)
        except Http404:
            return Response("No sprint available for inout project id.", status=status.HTTP_404_NOT_FOUND)

        try:
            paginator = PageNumberPagination()
            paginator.page_size = pagination_limit
            all_issues = IssueModel.objects.filter(sprint=sprint)
            result_page = paginator.paginate_queryset(all_issues, request)
            serializer = IssueSerializer(result_page, many=True)
            serializer_data = serializer.data
            issues = paginator.get_paginated_response(serializer_data)
            current_page_issues = issues.data['results']
            if len(current_page_issues) == 0:
                raise Exception("No issues present for this project")
            return Response(current_page_issues, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"error": "Page doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request, issue_id):

        issue_existence = Utils.get_object_by_id(IssueModel, issue_id)
        if issue_existence['status'] is False:
            return Response({'error': 'The issue does not exist'}, status=status.HTTP_404_NOT_FOUND)

        issue_status = request.GET.get('status')

        logger.info(f"issue status {issue_status}  {type(issue_status)}")

        if not issue_status:
            return Response({"error": "Params not passed properly"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            issue_obj = IssueModel.objects.get(id=issue_id)
            serializer = IssueSerializer(issue_obj, data={
                                         'status': issue_status.upper(), 'title': issue_obj.title, 'type': issue_obj.type})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ValidationError as error:
            return Response({"error": f"Params not passed properly. {error}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(f"Error : {error}", status=525)

    def delete(self, request, issue_id):
        """This API is to delete issue of given issue_id
        Args:
            request : None
            issue_id (str): issue id
        """
        logger.info(issue_id)
        try:
            issue_obj = IssueModel.objects.get(id=issue_id)
            issue_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except IssueModel.DoesNotExist:
            return Response({"error": "The issue does not exist"}, status=status.HTTP_404_NOT_FOUND)
