from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password


def generate_token(user):
    """This function generates token using django Session Store

    Returns:
        token : encoded data
    """
    token = Token.objects.create(user=user)
    print(token.key)
    return token.key


def validate_token(token):
    """
        This function is responsible for validating the token

        Parameters:
        - token : token is encoded key which is act as authorization for user.

        Returns:
        - User if token hasn't expire
        - False if token has expired
    """
    try:
        token = Token.objects.get(key=token)
        user = token.user
        return user
    except Token.DoesNotExist:
        return False


def authenticate_user(user, user_data):

    print(user.password)
    print(user_data['password'])

    auth = authenticate(
        username=user_data['username'], password=user_data['password'])

    print(f"login authenticate value {auth}")
    # TODO
    # if auth is None:
    #     print("password ok")
    #     return False
    return True
