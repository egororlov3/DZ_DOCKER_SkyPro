from django.core.management.base import BaseCommand
from study.models import Payment
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает тестовые платежи для пользователей'

    def handle(self, *args, **kwargs):
        # Создаем тестовых пользователей
        user1, created1 = User.objects.get_or_create(email='user1@sky.pro', defaults={
            'username': 'user1',
            'password': 'password1'
        })
        user2, created2 = User.objects.get_or_create(email='user2@sky.pro', defaults={
            'username': 'user2',
            'password': 'password2'
        })

        # Устанавливаем пароли
        if created1:
            user1.set_password('password1')
            user1.save()

        if created2:
            user2.set_password('password2')
            user2.save()

        # Тестовые данные
        payments = [
            {
                'user': user1,
                'payment_date': datetime(2024, 10, 1, 12, 0),
                'course_id': 2,
                'lesson': None,
                'amount': 5000.00,
                'payment_method': 'cash'
            },
            {
                'user': user2,
                'payment_date': datetime(2024, 10, 2, 13, 0),
                'course': None,
                'lesson_id': 4,
                'amount': 1500.00,
                'payment_method': 'tranzit'
            }
        ]

        # Запись данных в модель
        for payment in payments:
            Payment.objects.create(**payment)
            self.stdout.write(self.style.SUCCESS(f'Платеж от {payment["user"]} успешно добавлен.'))

        self.stdout.write(self.style.SUCCESS('Все платежи успешно добавлены.'))
