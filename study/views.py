from django_filters import rest_framework as filters
from rest_framework import viewsets, generics
from .models import Course, Lesson, Payment
from .permissions import IsStaff, IsSuper, IsAuthor
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated


# БАЗОВЫЕ ФОРМАТЫ ДЛЯ КОНТРОЛЛЕРОВ
class BaseCreateView(generics.CreateAPIView):
    """Базовый класс для создания объектов с проверкой прав доступа."""
    permission_classes = [IsSuper]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BaseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Базовый класс для получения, обновления и удаления объектов."""
    permission_classes = [IsStaff | IsAuthor]


# КУРСЫ
class CourseListView(generics.ListAPIView):
    """Получение списка курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
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


class CourseRetrieveView(BaseRetrieveUpdateDestroyView):
    """Получение определенного курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdateView(BaseRetrieveUpdateDestroyView):
    """Изменение курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDestroyView(generics.DestroyAPIView):
    """Удаление курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsSuper]


# УРОКИ
class LessonListView(generics.ListAPIView):
    """Получение списка уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsStaff | IsAuthor]


class LessonCreateView(BaseCreateView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        if not (user.is_staff or user.is_superuser):
            return self.queryset.filter(author=user)
        return self.queryset


class LessonRetrieveView(BaseRetrieveUpdateDestroyView):
    """Получение определенного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateView(BaseRetrieveUpdateDestroyView):
    """Изменение урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


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
