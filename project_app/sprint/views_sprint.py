from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..utils import Utils
from .sprint_serializer import SprintSerializer
from ..models import Sprint as SprintModel, Project as ProjectModel, Issue as IssueModel
import logging
logger = logging.getLogger(__name__)


class SprintView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This function is to create a sprint
        Args:
            request : The request object contain details for create sprint
        Return:
            Response: created project details
        """
        sprint_data = request.data
        project_id = sprint_data['project']
        if not project_id:
            return Response(sprint_data, status=status.HTTP_400_BAD_REQUEST)

        project_exits = Utils.get_object_by_id(ProjectModel, project_id)
        if project_exits['status'] == False:
            return Response({"project": project_exits['error'].format("project")}, status=status.HTTP_400_BAD_REQUEST)

        if Utils.validate_datetime_format(
                sprint_data['start_date']) == False:
            return Response({'start_date': f"Datetime has wrong format. Use one of these 	formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]. your data is {sprint_data['start_date']}"}, status=status.HTTP_400_BAD_REQUEST)

        if Utils.validate_datetime_format(
                sprint_data['end_date']) == False:
            return Response({'end_date': f"Datetime has wrong format. Use one of these 	formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]. your data is {sprint_data['end_date']}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SprintSerializer(data=sprint_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, sprint_id=None, *args, **kwargs):
        """This function is to get all sprints
        Args:
            request : sprint_id/None
        Return:
            Response: List/Single sprint details
        """
        if sprint_id:
            try:
                sprint = SprintModel.objects.get(id=sprint_id)
                sprint_data = sprint.__dict__
                del sprint_data['_state']
                return Response(sprint_data, status=status.HTTP_200_OK)
            except SprintModel.DoesNotExist:
                return Response({"error": "The sprint does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        all_sprints = SprintModel.objects.all()
        return Response(all_sprints.values(), status=status.HTTP_200_OK)

    def put(self, request):
        """This function is used for add given issues into the given sprint

        Args:
            request : It contain sprint id & list of issues

        Returns:
            Response: Put operation status True/error
        """
        sprint_id = request.data.get('sprint')
        issue_data = request.data.get('issues')

        if not sprint_id:
            return Response({"error": "No sprint id passed"}, status=status.HTTP_400_BAD_REQUEST)

        if not issue_data:
            return Response({"error": "No issue ids passed"}, status=status.HTTP_400_BAD_REQUEST)

        sprint_exits = Utils.get_object_by_id(SprintModel, sprint_id)

        if sprint_exits['status'] == False:
            return Response({"error": sprint_exits['error'].format(
                "sprint")}, status=status.HTTP_400_BAD_REQUEST)

        issue_list = []

        if isinstance(issue_data, str):
            issue_list.append(issue_data)
        elif isinstance(issue_data, list):
            issue_list = issue_data
        else:
            return Response({"error": "invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sprint_obj = SprintModel.objects.get(id=sprint_id)
            for issue in issue_list:
                issue_obj = IssueModel.objects.get(id=issue)
                issue_obj.sprint = sprint_obj
                issue_obj.save()
            return Response({"success": "True"}, status=status.HTTP_201_CREATED)
        except IssueModel.DoesNotExist as error:
            return Response({"error": f"Issues don't exist for the given issue ids {issue}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sprint_id):
        """This function is to delete sprints of given sprint_id
        Args:
            request : None
            sprint_id (str): sprint id
        Returns:
            Response: Delete operation status yes/error
        """
        logger.info(f"sprint id {sprint_id}")
        try:
            sprint = SprintModel.objects.get(id=sprint_id)
            sprint.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except SprintModel.DoesNotExist:
            return Response({"error": "The sprint does not exist"}, status=status.HTTP_400_BAD_REQUEST)
