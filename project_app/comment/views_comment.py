from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..utils import Utils
from ..models import Issue as IssueModel, Sprint as SprintModel, Comment as CommentModel
from ..project.project_utils import ProjectUtils
from .comment_serializer import CommentSerializer
import logging
logger = logging.getLogger(__name__)


class CommentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This function is used for create comment in given issue.

        Returns:
            Response: created comment details
        """
        issue_id = request.data.get('issue')
        user_id = request.data.get('user')
        comment_text = request.data.get('comment')

        if not issue_id or not user_id or not comment_text:
            return Response({"error": "issue/user/comment field may not be empty"}, status=status.HTTP_400_BAD_REQUEST)

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
            if is_user_active:
                serializer = CommentSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User is not active in this project'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'User is not a part of this project'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """This function is used for retrieve all comments

        Returns:
           Response: list of comments
        """
        all_comments = CommentModel.objects.all()
        return Response(all_comments.values(), status=status.HTTP_200_OK)

    def delete(self, request, comment_id):
        """This function is used for delete comment of given id. 

        Args:
            comment_id (str): This comment id of to be deleted Comment
        Returns:
            Response: Delete operation status yes/error
        """
        try:
            comment_obj = CommentModel.objects.get(
                id=comment_id)
            comment_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except CommentModel.DoesNotExist:
            return Response({"error": "The comment does not exist"}, status=status.HTTP_400_BAD_REQUEST)
