from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..utils import Utils
from ..models import Project as ProjectModel, User as UserModel, UserProjectRelation as UserProjectRelationModel
from .user_project_relation_serializer import UserProjectRelationSerializer
from ..project.project_utils import ProjectUtils

import logging
logger = logging.getLogger(__name__)


class UserProjectRelationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """This function is used for create relation between given user & project

        Args:
            request: it contain user id & project id

        Returns:
            Response: created user project relation details
        """
        request_data = request.data
        project_id = request_data['project']
        user = request_data['user']

        if not user or not project_id:
            return Response({"success": "False"}, status=status.HTTP_400_BAD_REQUEST)

        project_existence = Utils.get_object_by_id(ProjectModel, project_id)

        if project_existence['status'] is False:
            return Response({'error': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if isinstance(user, str) or isinstance(user, int):
            user_list = [user]
        else:
            user_list = user

        invalid_user = []
        valid_relation_data = []
        already_exists_user = []

        for user_id in user_list:
            user_existence = Utils.get_object_by_id(UserModel, user_id)
            if user_existence['status'] is False:
                invalid_user.append(user_id)
            elif ProjectUtils.user_existence_in_project(user_id, project_id) == False:
                serializer = UserProjectRelationSerializer(
                    data={
                        "project": project_id,
                        "user": user_id
                    })
                if serializer.is_valid():
                    serializer.save()
                    valid_relation_data.append(serializer.data)
            else:
                already_exists_user.append(user_id)
        logger.info(f"invalid users {invalid_user}")
        logger.info(f"users already exits in project  {already_exists_user}")
        return Response({"success": "True", "data": valid_relation_data}, status=status.HTTP_201_CREATED)

    def get(self, request, id=None, *args, **kwargs):
        """This function is used for get list of all users or of given project id

        Args:
            id (str): project id or Defaults to None.

        Returns:
            Response: List of user-project-relation or all user of given project id
        """
        project_id = id
        logger.info(f"inside get {id}")
        if project_id is None:
            all = UserProjectRelationModel.objects.all()
            return Response(all.values(), status=status.HTTP_200_OK)

        try:
            project_existence = Utils.get_object_by_id(
                ProjectModel, project_id)

            if project_existence['status'] is False:
                return Response({'error': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

            all_users_of_project = ProjectUtils.get_all_users_of_a_project(
                project_id)

            return Response(all_users_of_project.values(), status=status.HTTP_200_OK)
        except Exception as error:
            logger.info(
                f"error while fetching user project relation data. Error : {error}")
            return Response({"error": "error while fetching user project relation data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        """This function is for update user of a project

        Args:
            request (_type_): _description_
        """

        user_id = request.GET.get('user')
        project_id = request.GET.get('project')

        if not user_id:
            return Response({"error": "User param not passed"}, status=status.HTTP_400_BAD_REQUEST)

        if not project_id:
            return Response({"error": "Project param is not passed"}, status=status.HTTP_400_BAD_REQUEST)

        project_existence = Utils.get_object_by_id(ProjectModel, project_id)

        if project_existence['status'] is False:
            return Response({'error': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user_existence = Utils.get_object_by_id(UserModel, user_id)

        if user_existence['status'] is False:
            return Response({'error': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if ProjectUtils.user_existence_in_project(user_id, project_id) == False:
            return Response({"error": "No User Project Relation present for this project"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_project_relation = UserProjectRelationModel.objects.get(
                user=user_id, project=project_id)

            if user_project_relation.is_active == True:
                user_project_relation.is_active = False
            elif user_project_relation.is_active == False:
                user_project_relation.is_active = True
            user_project_relation.save()
            data = user_project_relation.__dict__
            del data['_state']
            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(f"Error while changing user status in project. {error}", status=525)

    def delete(self, request, id):
        """This function is to delete user-project-relation of given id
        Args:
            request : None
            id (str): user-project-relation id
        Returns:
            Response: Delete operation status yes/error
        """
        user_project_relation_id = id

        try:
            user_project_relation_obj = UserProjectRelationModel.objects.get(
                id=user_project_relation_id)
            user_project_relation_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except UserProjectRelationModel.DoesNotExist:
            return Response({"error": "The user project relation does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            logger.info(
                f"error while deleting user project relation data. Error : {error}")
            return Response({"error": "error while deleting user project relation data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
