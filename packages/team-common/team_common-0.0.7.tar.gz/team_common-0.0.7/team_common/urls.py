from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, TitleViewSet, DepartmentViewSet,)

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('title', TitleViewSet)
router.register('department', DepartmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
