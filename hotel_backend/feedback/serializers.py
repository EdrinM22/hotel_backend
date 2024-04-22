from rest_framework import serializers
from .models import Feedback


class FeedBackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('stars', 'text', 'guest')


class FeedBackListSerializer(serializers.ModelSerializer):
    guest = serializers.SerializerMethodField()

    class Meta:
        model = Feedback
        fields = ('id', 'stars', 'text', 'guest')

    def get_guest(self, obj: Feedback):
        return obj.guest
