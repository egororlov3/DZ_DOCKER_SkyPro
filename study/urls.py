from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import StudyConfig
from .views import LessonListView, LessonCreateView, LessonRetrieveView, LessonUpdateView, \
    LessonDestroyView, PaymentViewSet, CourseListView, CourseCreateView, CourseRetrieveView, CourseUpdateView, \
    CourseDestroyView, SubscribeCourseView, UnsubscribeCourseView, CreatePaymentIntentView, RetrievePaymentIntentView

app_name = StudyConfig.name


router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    # Уроки
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', LessonDestroyView.as_view(), name='lesson-delete'),

    # Подписка/Отписка
    path('subscribe/<int:course_id>/', SubscribeCourseView.as_view(), name='subscribe-course'),
    path('unsubscribe/<int:course_id>/', UnsubscribeCourseView.as_view(), name='unsubscribe-course'),

    # Курсы
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/', CourseRetrieveView.as_view(), name='course-detail'),
    path('courses/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', CourseDestroyView.as_view(), name='course-delete'),

    # STRIPE
    path('payment-intent-create/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('payment-intent-retrieve/<str:payment_intent_id>/', RetrievePaymentIntentView.as_view(), name='retrieve-payment-intent'),
] + router.urls
