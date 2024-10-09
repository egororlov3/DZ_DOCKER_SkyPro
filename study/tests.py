from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course, Lesson, Subscription
from users.models import User


class LessonTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Курс 1', description='Описание курса 1')
        self.lesson = Lesson.objects.create(title='Урок 1', description='Описание урока 1', course=self.course)

    def test_create_lesson(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('study:lesson-create')
        data = {
            "title": "Урок 2",
            "description": "Описание урока 2",
            "course": self.course.id,
            "video_url": "https://youtube.com/example"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_lessons(self):
        url = reverse('study:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Проверяем, что вернул один урок

    def test_update_lesson(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('study:lesson-update', args=[self.lesson.id])
        data = {
            "title": "Обновленный урок",
            "description": "Обновленное описание",
            "course": self.course.id,
            "video_url": "https://youtube.com/example"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('study:lesson-delete', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(title='Курс 1', description='test1')

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        response = self.client.post(reverse('study:subscribe-course', args=[self.course.id]), {
            'user': self.user.id,
            'course': self.course.id,
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.login(username='testuser', password='testpassword')
        url = reverse('study:unsubscribe-course', args=[self.course.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_is_subscribed(self):
        self.client.force_authenticate(user=self.user)
        self.client.login(username='testuser', password='testpassword')
        url = reverse('study:course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['results'][0]['is_subscribed'])  # Проверяем, что поле is_subscribed False


