from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializer import User, UserSerializer
from .auth_utils import generate_token, validate_token, authenticate_user
import logging
logger = logging.getLogger(__name__)


class UserUtils():
    def create_user(user_data):

        serializer = UserSerializer(data=user_data)
        logger.info(f"serializer is_valid : {serializer.is_valid()}")

        if serializer.is_valid():

            new_created_user = serializer.save()

            # token generate for current user
            token = generate_token(new_created_user)

            new_user_data = serializer.data

            return {'status': False, 'msg': {'token': token, 'data': new_user_data}, 'response_code': status.HTTP_201_CREATED}

        else:
            return {'status': False, 'msg': "Bad request", 'response_code': status.HTTP_400_BAD_REQUEST}

    def check_user_existence(username=None, id=None):
        try:
            if id != None:
                user = get_object_or_404(User, id=id)
            elif username != None and isinstance(username, str):
                user = User.objects.get(username=username)
            elif id != None and username != None and isinstance(username, str):
                user = User.objects.get(id=id, username=username)
            return user
        except User.DoesNotExist:
            return None

    def user_login(user_data):

        user = User.objects.get(username=user_data.get('username'))

        if user is None:
            return {'status': False, 'msg': "invalid username. User not found.", 'response_code': status.HTTP_400_BAD_REQUEST}

        auth_res = authenticate_user(user, user_data)

        if auth_res:
            
            token = user.auth_token.key
            validated_user = validate_token(token)
            if validated_user == False:
                token = generate_token(user=user)
            return {'status': True, 'msg': token, 'response_code': status.HTTP_200_OK}
        else:
            return {'status': False, 'msg': "invalid password.", 'response_code': status.HTTP_401_UNAUTHORIZED}
