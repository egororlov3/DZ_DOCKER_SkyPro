from django.conf import settings
from django.db import models

from users.models import NULLABLE, User


# КУРС
class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='название')
    image = models.ImageField(upload_to='study/', **NULLABLE, verbose_name='картинка')
    description = models.TextField(verbose_name='описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


# ПОДПИСКА
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')

    def __str__(self):
        return f'{self.user.username} subscribed to {self.course.title}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'


# УРОК
class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='курсы',
                               default=1)
    title = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='study/', **NULLABLE, verbose_name='картинка')
    video_url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


# ПЛАТЕЖ
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('tranzit', 'Перевод на счет'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(Course, **NULLABLE, on_delete=models.CASCADE, verbose_name='оплаченный курс')
    lesson = models.ForeignKey(Lesson, **NULLABLE, on_delete=models.CASCADE, verbose_name='оплаченный урок')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'Платеж от {self.user} - {self.amount} за {self.course if self.course else self.lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
