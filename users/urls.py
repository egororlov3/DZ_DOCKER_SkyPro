from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = router.urls
