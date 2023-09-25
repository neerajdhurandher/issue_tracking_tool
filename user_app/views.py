import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import User
from .user_utils import UserUtils as user_utils
from .models import User as UserModel
import logging
logger = logging.getLogger(__name__)


class UserView(APIView):

    def post(self, request):
        """This function is used for create a user.

        Args:
            request : The request object contains user details 
        Return:
            Response: created user details
        """

        user_data = request.data

        logger.info(f"user input : {user_data}")
        user_obj = None

        try:
            user_obj = UserModel.objects.get(username=user_data['username'])
        except UserModel.DoesNotExist:
            logger.info("user not exist")

        logging.info(f"user exits {user_obj}")

        if user_obj is None:
            user_create_res = user_utils.create_user(request.data)

            return Response(user_create_res.get('msg'), status=user_create_res.get('response_code'))
        else:
            login_data = user_utils.user_login(request.data)
            if login_data['status']:
                return Response({
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "token": login_data['msg']
                }, status=status.HTTP_200_OK)
            else:
                return Response(login_data['msg'], status=login_data['response_code'])

    def get(self, request, user_id):
        """This function is used for get user of given id

        Args:
            user_id (str):

        Returns:
            Response : User detail of given user id
        """

        user_exits_value = user_utils.check_user_existence(id=user_id)

        if user_exits_value is None:
            return Response({"error": "User with this id doesn't exist"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            user_details = user_exits_value.__dict__
            del user_details['_state']
            return Response(user_details, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        """This function is to delete user of given id
        Args:
            request : None
            user_id (str):
        Returns:
            Response: Delete operation status yes/error
        """
        try:
            user_obj = UserModel.objects.get(id=user_id)
            user_obj.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except UserModel.DoesNotExist:
            return Response({"error": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND)


class GetAllUserView(APIView):
    def get(self, request):
        """This function is used for get all users

        Returns:
            Response: List of all users
        """
        all_user = User.objects.all()
        return Response(all_user.values(), status=status.HTTP_200_OK)
