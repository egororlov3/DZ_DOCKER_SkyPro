import stripe
from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework import viewsets, generics
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Lesson, Payment, Subscription
from .pagination import StudyPagination
from .permissions import IsStaff, IsSuper, IsAuthor
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer
from study.tasks import send_subscription_confirmation_email, send_unsubscribe_confirmation_email

stripe.api_key = settings.STRIPE_SECRET_KEY


# ПЛАТЕЖИ STRIPE
class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Получаем сумму и валюту из запроса
            amount = request.data.get('amount')
            currency = request.data.get('currency', 'usd')

            # Создаем PaymentIntent через API Stripe
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
            )

            return Response({
                'client_secret': intent['client_secret']
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class RetrievePaymentIntentView(APIView):
    def get(self, request, payment_intent_id, *args, **kwargs):
        try:
            # Получаем платеж по ID
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Возвращаем информацию о платеже
            return Response({
                'payment_intent': intent
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)


# БАЗОВЫЕ ФОРМАТЫ ДЛЯ КОНТРОЛЛЕРОВ
class BaseCreateView(generics.CreateAPIView):
    """Базовый класс для создания объектов с проверкой прав доступа."""
    permission_classes = [IsSuper]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# КУРСЫ
class CourseListView(generics.ListAPIView):
    """Получение списка курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StudyPagination
    permission_classes = [IsStaff | IsAuthor]


class CourseCreateView(BaseCreateView):
    """Создание курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            return self.queryset.filter(author=user)
        return self.queryset


class CourseRetrieveView(RetrieveAPIView):
    """Получение определенного курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdateView(UpdateAPIView):
    """Изменение курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsStaff | IsAuthor]


class CourseDestroyView(generics.DestroyAPIView):
    """Удаление курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsSuper]


# ПОДПИСКА НА КУРС
class SubscribeCourseView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        subscription = serializer.save(user=self.request.user)  # Сохраняем подписку

        # Отправляем письмо после успешной подписки
        send_subscription_confirmation_email.delay(self.request.user.email, subscription.course.title)


class UnsubscribeCourseView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_object(self):
        return generics.get_object_or_404(self.queryset, user=self.request.user, course=self.kwargs['course_id'])

    def perform_destroy(self, instance):
        # Отправляем письмо перед удалением подписки
        send_unsubscribe_confirmation_email.delay(self.request.user.email, instance.course.title)
        instance.delete()


# УРОКИ
class LessonListView(generics.ListAPIView):
    """Получение списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsStaff | IsAuthor]
    pagination_class = StudyPagination


class LessonCreateView(BaseCreateView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            return self.queryset.filter(author=user)
        return self.queryset


class LessonRetrieveView(RetrieveAPIView):
    """Получение определенного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsStaff | IsAuthor]


class LessonUpdateView(UpdateAPIView):
    """Изменение урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsStaff | IsAuthor]


class LessonDestroyView(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsSuper]


# ОПЛАТА
class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name='course__id')
    lesson = filters.NumberFilter(field_name='lesson__id')
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)
    payment_date = filters.DateTimeFilter(field_name='payment_date')

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method', 'payment_date']


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter
    permission_classes = [IsSuper]
