from rest_framework.serializers import ModelSerializer
from .models import CustomUser
from game_app.models import Game


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password','name', 'surname', 'phone', ]

    def create(self, validated_data):
        user = CustomUser.object.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'phone', 'wallet', 'birth_date', 'age','number_of_purchases']


class UserProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'phone', 'birth_date', 'age']

