# study/validators.py
import re
from rest_framework import serializers


def validate_youtube_url(value):
    # Проверяем, что ссылка ведет на youtube.com
    if 'youtube.com' not in value:
        raise serializers.ValidationError('Тут могут быть только ссылки на youtube.com.')

    return value
