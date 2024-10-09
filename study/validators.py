from rest_framework import serializers
from study.models import Subscription


def validate_youtube_url(value):
    # Проверяем, что ссылка ведет на youtube.com
    if 'youtube.com' not in value:
        raise serializers.ValidationError('Тут могут быть только ссылки на youtube.com.')

    return value


def validate_is_subscribed(course, request):
    # Проверяем подписку пользователя
    if request and request.user.is_authenticated:
        return Subscription.objects.filter(user=request.user, course=course).exists()
    return False
