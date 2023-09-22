from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password',)

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        user = super().create(validated_data)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('password', None)
        return data
