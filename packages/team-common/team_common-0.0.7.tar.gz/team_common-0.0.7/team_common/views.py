from rest_framework import viewsets
from .serializers import (TitleSerializer, DepartmentSerializer, UserSerializer)
from .models import (Title, Department, User)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return TitleSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()

    def get_serializer_class(self):
        return DepartmentSerializer