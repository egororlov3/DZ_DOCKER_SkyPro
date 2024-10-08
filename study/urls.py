from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import StudyConfig
from .views import LessonListView, LessonCreateView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView, PaymentViewSet, CourseListView, CourseCreateView, CourseRetrieveView, CourseUpdateView, \
    CourseDestroyView

app_name = StudyConfig.name


router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson-delete'),

    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseRetrieveView.as_view(), name='course-detail'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', CourseDestroyView.as_view(), name='course-delete'),
] + router.urls
