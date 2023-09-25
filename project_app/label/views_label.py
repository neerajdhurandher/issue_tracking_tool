from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..utils import Utils
from ..models import Issue as IssueModel, Label as LabelModel
from .label_serializer import LabelSerializer
import logging
logger = logging.getLogger(__name__)


class LabelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This function is used for create label of given data.

        Returns:
            Response: Details of created label
        """
        issue_id = request.data.get('issue')
        label_text = request.data.get('label')

        if not issue_id or not label_text:
            return Response({"issue/label field may not be empty"}, status=status.HTTP_400_BAD_REQUEST)

        issue_existence = Utils.get_object_by_id(IssueModel, issue_id)
        if issue_existence['status'] is False:
            return Response({'error': 'The issue does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """This function is used for get all labels.

        Returns:
            Response: List of labels
        """
        all_labels = LabelModel.objects.all()
        return Response(all_labels.values(), status=status.HTTP_200_OK)

    def delete(self, request, label_id):
        """This function is used for delete label of given id

        Args:
            label_id (str): label id for delete

        Returns:
            Response: Delete operation status yes/error
        """
        try:
            label_obj = LabelModel.objects.get(
                id=label_id)
            label_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except LabelModel.DoesNotExist:
            return Response({"error": "The label does not exist"}, status=status.HTTP_404_NOT_FOUND)
