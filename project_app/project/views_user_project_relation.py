from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from ..utils import Utils
from ..models import Project as ProjectModel, User as UserModel, UserProjectRelation as UserProjectRelationModel
from .user_project_relation_serializer import UserProjectRelationSerializer
from .project_utils import ProjectUtils

import logging
logger = logging.getLogger(__name__)


class UserProjectRelationView(APIView):
    def post(self, request):
        request_data = request.data
        project_id = request_data['project']
        user = request_data['user']

        if not user or not project_id:
            return Response({"success": "False"}, status=status.HTTP_400_BAD_REQUEST)

        project_existence = Utils.get_object_by_id(ProjectModel, project_id)

        if project_existence['status'] is False:
            return Response({'error': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if isinstance(user, str):
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
                    data=request_data)
                if serializer.is_valid():
                    serializer.save()
                    valid_relation_data.append(serializer.data)
            else:
                already_exists_user.append(user_id)
        return Response({"success": "True", "data": valid_relation_data},status=status.HTTP_201_CREATED)

    def get(self, request):
        all = UserProjectRelationModel.objects.all()
        return Response(all.values(), status=status.HTTP_200_OK)


    def put(self, request):
        """This API is for update user of a project

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

    def delete(self, request, userprojectrelation_id):
        user_project_relation_id = userprojectrelation_id

        try:
            user_project_relation_obj = UserProjectRelationModel.objects.get(
                id=user_project_relation_id)
            user_project_relation_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except UserProjectRelationModel.DoesNotExist:
            return Response({"error": "The user project relation does not exist"}, status=status.HTTP_404_NOT_FOUND)

class UserProjectRelationByIDView(APIView):
    def get(self, request, project_id):
        project_existence = Utils.get_object_by_id(ProjectModel, project_id)

        if project_existence['status'] is False:
            return Response({'error': 'The project does not exist'}, status=status.HTTP_404_NOT_FOUND)

        all_users_of_project = ProjectUtils.get_all_users_of_a_project(
            project_id)

        return Response(all_users_of_project.values(), status=status.HTTP_200_OK)
