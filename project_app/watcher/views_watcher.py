from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..utils import Utils
from ..models import Issue as IssueModel, Sprint as SprintModel, Watcher as WatcherModel
from ..project.project_utils import ProjectUtils
from .watcher_serializer import WatcherSerializer
import logging
logger = logging.getLogger(__name__)


class WatcherView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This function is used to create watcher to given user for a given issue.  

        Args:
            request: it contain user id & issue id
        Returns:
            Response: created watcher details
        """
        issue_id = request.data.get('issue')
        user_id = request.data.get('user')
        if not (issue_id or user_id or isinstance(issue_id, str) or isinstance(user_id, str)):
            return Response({"error": "issue/user field may not be empty"}, status=status.HTTP_400_BAD_REQUEST)

        issue_existence = Utils.get_object_by_id(IssueModel, issue_id)
        if issue_existence['status'] is False:
            return Response({'error': 'The issue does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        issue_sprint_id = issue_existence['data']['sprint_id']
        if issue_sprint_id is None:
            return Response({'error': 'The issue does not tagged with any project'}, status=status.HTTP_400_BAD_REQUEST)

        sprint_obj = Utils.get_object_by_id(SprintModel, issue_sprint_id)

        project_id = sprint_obj['data']['project_id']

        user_project_relation_existence = ProjectUtils.user_existence_in_project(
            user_id, project_id)

        if user_project_relation_existence:
            is_user_active = ProjectUtils.get_user_status_in_project(
                user_id, project_id)
            watcher_existence = WatcherModel.objects.filter(
                user=user_id, issue=issue_id)
            if len(watcher_existence.values()) > 0:
                return Response({"error": f"`{user_id}` user is already watcher of `{issue_id}` issue."}, status=status.HTTP_400_BAD_REQUEST)
            if is_user_active:
                serializer = WatcherSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'User is not active in this project'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User is not a part of this project'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """This function is used for get all watcher list

        Returns:
            Response: List of watchers.
        """
        all_watchers = WatcherModel.objects.all()
        return Response(all_watchers.values(), status=status.HTTP_200_OK)

    def put(self, request):
        """This function is used for update user status in watcher

        Args:
            request : it contain user id & issue id

        Returns:
            Response : updated watcher details
        """
        user_id = request.GET.get('user')
        issue_id = request.GET.get('issue')

        if not issue_id or not user_id or not isinstance(issue_id, str) or not isinstance(user_id, str):
            return Response({"issue": "issue param not passed", "user": "User param not passed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            watcher_obj = WatcherModel.objects.get(
                user=user_id, issue=issue_id)
            if watcher_obj.is_active == True:
                watcher_obj.is_active = False
            elif watcher_obj.is_active == False:
                watcher_obj.is_active = True
            watcher_obj.save()
            data = watcher_obj.__dict__
            del data['_state']
            return Response(data, status=status.HTTP_201_CREATED)
        except WatcherModel.DoesNotExist as error:
            return Response({"error": "watcher with id not exits."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({"error": f"Error while changing user's watching status in issue. {error}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, watcher_id):
        """This function is to delete watcher of given sprint_id
        Args:
            request : None
            watcher_id (str): watcher id
        Returns:
            Response: Delete operation status yes/error
        """
        try:
            watcher_obj = WatcherModel.objects.get(
                id=watcher_id)
            watcher_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except WatcherModel.DoesNotExist:
            return Response({"error": "The watcher does not exist"}, status=status.HTTP_400_BAD_REQUEST)
