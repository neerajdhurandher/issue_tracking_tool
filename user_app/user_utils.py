from rest_framework import status
from .serializer import User, UserSerializer
from .auth_utils import generate_token
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class UserUtils():
    def create_user(user_data):

        serializer = UserSerializer(data=user_data)

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
                user = User.objects.get(id=id)
            elif username != None and isinstance(username, str):
                user = User.objects.get(username=username)
            elif id != None and username != None and isinstance(username, str):
                user = User.objects.get(id=id, username=username)
            return user
        except User.DoesNotExist:
            return None

    def user_login(user_data):

        user_obj = User.objects.get(username=user_data.get('username'))

        logger.info(f"input {user_data['password']}")
        logger.info(f"stored {user_obj.password}")

        logger.info(f"user pass {user_obj.has_usable_password()}")

        auth_res = True if user_data['password'] == user_obj.password else False

        logger.info(f"auth {auth_res}")
        if auth_res:
            token = user_obj.auth_token.key
            user_obj.last_login = datetime.now()
            user_obj.save()
            return {'status': True, 'msg': token, 'response_code': status.HTTP_200_OK}
        else:
            return {'status': False, 'msg': "invalid password.", 'response_code': status.HTTP_401_UNAUTHORIZED}
