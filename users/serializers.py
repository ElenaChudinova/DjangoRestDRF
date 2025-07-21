from rest_framework import serializers

from users.models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "password", "phone", "city", "avatar")


class PaymentSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    def get_course_name(self, obj):
        return obj.courses.name

    class Meta:
        model = Payment
        fields = "__all__"
