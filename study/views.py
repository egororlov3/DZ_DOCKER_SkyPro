from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


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
