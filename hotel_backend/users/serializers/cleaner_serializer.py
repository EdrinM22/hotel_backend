from rest_framework import serializers
from users.models import Cleaner, User
from .user_serializer import UserCreateSerializer



class CleanerCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    class Meta:
        model = Cleaner
        fields = ('user', 'resume', 'notes', 'photo')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        username: str = str(user_data.get('first_name')[0]) + '.' + user_data.get('last_name')
        counter: int = 1
        while User.objects.filter(username=username).exists():
            username = username + str(counter) if counter == 1 else username[0: -1] + str(counter)
            counter += 1
        user = User.objects.create_user(username=username, **user_data)
        raise Exception('Ome')
        cleaner = Cleaner.objects.create(user=user, **validated_data)
        return cleaner