from django.db import models

from users.models import NULLABLE


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    image = models.ImageField(upload_to='study/', **NULLABLE, verbose_name='картинка')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='study/', **NULLABLE, verbose_name='картинка')
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
