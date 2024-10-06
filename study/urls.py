from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import StudyConfig
from .views import CourseViewSet, LessonListView, LessonCreateView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView


app_name = StudyConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson-delete'),
] + router.urls
