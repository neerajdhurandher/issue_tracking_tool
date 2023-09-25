from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User
import bcrypt


def generate_token(user):
    """This function generates token using django Session Store

    Returns:
        token : encoded data
    """
    token, _ = Token.objects.get_or_create(user=user)
    print(str(token))
    return str(token)


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
        return True
    except Token.DoesNotExist:
        return False
