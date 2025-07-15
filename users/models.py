from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        max_length=50, unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    CASH = "НАЛИЧНЫЕ"
    BANK_TRANSFER = "ПЕРЕВОД НА СЧЕТ"
    PAYMENT_METHOD = (
        (CASH, "НАЛИЧНЫЕ"),
        (BANK_TRANSFER, "ПЕРЕВОД НА СЧЕТ"),
    )

    email = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_payment = models.DateTimeField(
        editable=False,
        verbose_name="Дата оплаты",
        null=True,
        blank=True,
    )
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=15,
        choices=PAYMENT_METHOD,
        default=CASH,
        verbose_name="Способ оплаты",
    )

    def __str__(self):
        return f"{self.paid_course if self.paid_course else self.paid_lesson} - {self.payment_amount}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ("date_payment",)


class Subscription(models.Model):
    sub_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="sub_user",
        null=True,
        blank=True,
    )
    sub_course = models.ForeignKey(
        "materials.Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="sub_course",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.sub_user, self.sub_course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        unique_together = (
            "sub_user",
            "sub_course",
        )
