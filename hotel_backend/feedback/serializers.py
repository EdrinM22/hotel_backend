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


class FeedBackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('stars', 'text')
        extra_kwargs = {
            'stars': {'allow_null': True,
                      'required': False}
        }


    def update(self, instance: Feedback, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.stars = validated_data.get('stars', instance.stars)
        instance.save()
        return instance
