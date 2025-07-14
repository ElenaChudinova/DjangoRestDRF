from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_forbidden_video


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_forbidden_video])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, source="courses")
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, obj):
        return obj.courses.count()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, obj):
        return obj.courses.count()
