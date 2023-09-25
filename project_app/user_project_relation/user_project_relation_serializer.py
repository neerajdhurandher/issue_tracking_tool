from rest_framework import serializers

from ..models import UserProjectRelation


class UserProjectRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjectRelation
        fields = "__all__"
