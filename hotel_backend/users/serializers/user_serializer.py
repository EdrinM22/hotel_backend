from rest_framework import serializers
from users.models import User

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'fathers_name', 'last_name',
                  'email', 'password', 'birthday', 'birthplace',
                  'personal_number', 'gender', 'phone_number')
