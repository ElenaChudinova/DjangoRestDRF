from rest_framework.serializers import ValidationError

forbidden_video = ["^(https?://)?(www\.)?youtube\.com/?$"]

def validate_forbidden_video(value):
    if value in forbidden_video:
        raise ValidationError("Невозможно загрузить данное видео, допустимые ссылки на youtube.com")