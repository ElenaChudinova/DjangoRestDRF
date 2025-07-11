from django.db import models


class Course(models.Model):
    id = models.AutoField(
        auto_created=True, primary_key=True, verbose_name="ID Курса"
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Укажите описание курса",
    )
    photo = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Укажите описание урока",
    )
    photo = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите картинку",
    )
    video = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
        help_text="Загрузите видео",
    )
    courses = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name= "courses",
        verbose_name="Курс",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"