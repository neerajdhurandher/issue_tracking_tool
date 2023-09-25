from rest_framework import serializers
from ..models import Watcher


class WatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watcher
        fields = "__all__"
        