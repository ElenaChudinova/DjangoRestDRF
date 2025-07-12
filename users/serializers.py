from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #
    #         email=validated_data["email"],
    #         password=validated_data["password"],
    #     )
    #     return user


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
