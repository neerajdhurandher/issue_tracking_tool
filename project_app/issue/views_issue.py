from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound, ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from ..utils import Utils
from .issue_serializer import IssueSerializer
from ..models import Issue as IssueModel, Sprint as SprintModel, Project as ProjectModel, User as UserModel
from ..constants import pagination_limit
from ..project.project_utils import ProjectUtils
import logging
logger = logging.getLogger(__name__)


class IssueView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        issue_data = request.data

        if not issue_data['title']:
            return Response({"title": "This field may not be blank"}, status=status.HTTP_400_BAD_REQUEST)

        sprint_id = issue_data['sprint']

        if not sprint_id:
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
        user_id = request.GET.get('assignee')

        if not page_no:
            return Response({"error": "Page param not passed"}, status=status.HTTP_400_BAD_REQUEST)

        if not project_id and not user_id:
            return Response({"error": "Project/Assignee param is not passed"}, status=status.HTTP_400_BAD_REQUEST)

        if not project_id and user_id:
            return self.get_all_issue_of_user(user_id, request)

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
            if len(all_issues.values()) == 0:
                return Response(
                    {"error": "No issues present for this project"}, status=status.HTTP_404_NOT_FOUND)
            result_page = paginator.paginate_queryset(all_issues, request)
            serializer = IssueSerializer(result_page, many=True)
            serializer_data = serializer.data
            issues = paginator.get_paginated_response(serializer_data)
            current_page_issues = issues.data['results']
            return Response(current_page_issues, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"error": "Page doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, issue_id):

        issue_existence = Utils.get_object_by_id(IssueModel, issue_id)
        if issue_existence['status'] is False:
            return Response({'error': 'The issue does not exist'}, status=status.HTTP_404_NOT_FOUND)

        issue_status = request.GET.get('status')
        user_id = request.GET.get('assignee')

        if not issue_status:
            if user_id:
                return self.assign_user_to_issue(issue_id, user_id)
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

    def assign_user_to_issue(self, issue_id, user_id):

        user_existence = Utils.get_object_by_id(UserModel, user_id)
        if user_existence['status'] is False:
            return Response({'error': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        issue_existence = Utils.get_object_by_id(IssueModel, issue_id)
        issue_sprint_id = issue_existence['data']['sprint_id']

        sprint_obj = Utils.get_object_by_id(SprintModel, issue_sprint_id)

        project_id = sprint_obj['data']['project_id']

        user_project_relation_existence = ProjectUtils.user_existence_in_project(
            user_id, project_id)

        if user_project_relation_existence:
            is_user_active = ProjectUtils.get_user_status_in_project(
                user_id, project_id)
            if is_user_active:
                issue_update = IssueModel.objects.get(id=issue_id)
                user_obj = UserModel.objects.get(id=user_id)
                issue_update.assignee = user_obj
                issue_update.save()
                updated_issue = issue_update.__dict__
                del updated_issue['_state']
                return Response(updated_issue, status=status.HTTP_201_CREATED)

            else:
                return Response({'error': 'User is not active in this project'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'User is not a part of this project'}, status=status.HTTP_400_BAD_REQUEST)

    def get_all_issue_of_user(self, user_id, request):
        user_existence = Utils.get_object_by_id(UserModel, user_id)
        if user_existence['status'] == False:
            return Response({"error": "User with this id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        try:

            paginator = PageNumberPagination()
            paginator.page_size = pagination_limit
            all_issues = IssueModel.objects.filter(assignee_id=user_id)
            if len(all_issues.values()) == 0:
                return Response(
                    {"error": "No issues assigned to this assignee"}, status=status.HTTP_404_NOT_FOUND)
            result_page = paginator.paginate_queryset(all_issues, request)
            serializer = IssueSerializer(result_page, many=True)
            serializer_data = serializer.data
            issues = paginator.get_paginated_response(serializer_data)
            current_page_issues = issues.data['results']
            return Response(current_page_issues, status=status.HTTP_200_OK)
        except NotFound as e:
            return Response({"error": "Page doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            logger.info(
                f"error while fetching issues of a user. Error : {error}")
            return Response({"error": "error while fetching issues of a user"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MultipleQueryIssueList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            data = request.GET

            and_params = {}
            for key in data:
                if 'and_' in key:
                    new_key = key.split("and_")[-1]
                    if new_key == "project":
                        new_key = "sprint__project__id"
                    if new_key == "assignee":
                        new_key = "assignee__id"
                    and_params[new_key] = data[key]
            queryset = IssueModel.objects.filter(
                **and_params).select_related('assignee', 'sprint')

            or_params = {}
            for key in data:
                if 'or_' in key:
                    new_key = key.split("or_")[-1]
                    if new_key == "project":
                        new_key = "sprint__project__id"
                    if new_key == "assignee":
                        new_key = "assignee__id"
                    or_params[new_key] = data[key]
                    queryset = queryset | IssueModel.objects.filter(
                        **or_params).select_related('assignee', 'sprint')

            response = IssueSerializer(queryset, many=True)
            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(
                f"Exception while searching for issue using multiple parameter: {str(e)}")
            return Response({"error": "Some problem occurred while searching for issues"}, status=400)
