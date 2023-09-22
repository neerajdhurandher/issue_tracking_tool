import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core import serializers
from .serializer import User, UserSerializer
from .user_utils import UserUtils as user_utils
import logging
logger = logging.getLogger(__name__)


class LoginUser(APIView):

    def post(self, request):
        """This API is to create a user.

        Args:
            request : The request object contains user details 
        """

        user_data = {}
        user_data['username'] = request.data.get('username')
        user_data['password'] = request.data.get('password')
        user_data['email'] = request.data.get('email')

        logger.info(f"user input : {user_data}")

        # check for exiting user
        user_exits_value = user_utils.check_user_existence(
            username=user_data['username'])

        logging.info(f"user exits {user_exits_value}")

        if user_exits_value is None:
            user_create_res = user_utils.create_user(user_data)

            return Response(user_create_res.get('msg'), status=user_create_res.get('response_code'))
        else:
            login_data = user_utils.user_login(user_data)
            if login_data['status']:
                return Response({
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "token": login_data['msg']
                }, status=status.HTTP_200_OK)
            else:
                return Response(login_data['msg'], status=login_data['response_code'])


class GetAllUsers(APIView):
    def get(self, request):
        all_user = User.objects.all()
        return Response(all_user.values(), status=status.HTTP_200_OK)


class GetUserByID(APIView):
    def get(self, request, user_id):
        user_exits_value = user_utils.check_user_existence(id=user_id)

        if user_exits_value is None:
            return Response({"error": "User with this id doesn't exist"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            user_details = user_exits_value.__dict__
            del user_details['_state']
            return Response(user_details, status=status.HTTP_200_OK)


class DeleteUser(APIView):

    def delete(self, request, user_id):
        logger.info("inside delete fun.")
        user = user_utils.check_user_existence(id=user_id)

        if user is None:
            return Response({"error": "The user does not exist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            user.delete()
            return Response({"success": "yes"}, status=status.HTTP_200_OK)
        except Exception as error:
            logging.error(f"Exception in delete user API: {error}")
            return Response("Error while deleting user.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    