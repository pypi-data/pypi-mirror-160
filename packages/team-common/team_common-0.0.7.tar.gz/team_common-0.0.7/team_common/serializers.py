from rest_framework import serializers
from .models import (User, Title, Department)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstName', 'lastName',
                  'profilePicture', 'username', 'userType', 'fullName']


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ["id", "name", "description", ]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name", "description", "numbOfEmployees"]
