from django_filters import rest_framework as filters
from rest_framework import viewsets, generics
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListView(generics.ListAPIView):
    """Получение списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateView(generics.CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveView(generics.RetrieveAPIView):
    """Получение определенного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateView(generics.UpdateAPIView):
    """Изменение урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyView(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


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
