from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_forbidden_video
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_forbidden_video])

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, source="courses")
    count_lesson = serializers.SerializerMethodField()
    sign_up = SubscriptionSerializer(many=True, source="sub_user", read_only=True)

    def get_count_lesson(self, obj):
        return obj.courses.count()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    def get_sign_up(self, obj):
        request = self.context.get("request")
        user = None
        if request:
            user = request.user
        return obj.sub_user.filter(user=user).exists()

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "lessons",
            "count_lesson",
            "sign_up",
        )


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, obj):
        return obj.courses.count()
