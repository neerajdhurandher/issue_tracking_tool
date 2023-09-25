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
        issue_id = request.data.get('issue')
        user_id = request.data.get('user')

        if not issue_id or not user_id:
            return Response({"issue/user field may not be empty"}, status=status.HTTP_400_BAD_REQUEST)

        issue_existence = Utils.get_object_by_id(IssueModel, issue_id)
        if issue_existence['status'] is False:
            return Response({'error': 'The issue does not exist'}, status=status.HTTP_404_NOT_FOUND)

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

        return Response("ok", 200)

    def get(self, request):
        all_watchers = WatcherModel.objects.all()
        return Response(all_watchers.values(), status=status.HTTP_200_OK)

    def put(self, request):
        user_id = request.GET.get('user')
        issue_id = request.GET.get('issue')

        if not user_id:
            return Response({"error": "User param not passed"}, status=status.HTTP_400_BAD_REQUEST)

        if not issue_id:
            return Response({"error": "Issue param is not passed"}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(f"Error while changing user's watching status in issue. {error}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, watcher_id):

        try:
            watcher_obj = WatcherModel.objects.get(
                id=watcher_id)
            watcher_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except WatcherModel.DoesNotExist:
            return Response({"error": "The watcher does not exist"}, status=status.HTTP_404_NOT_FOUND)
