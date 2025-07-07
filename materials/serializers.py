from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = SerializerMethodField()
    count_lesson = SerializerMethodField()

    def get_count_lesson(self, course):
        return Course.objects.filter(lesson=course.lesson).count()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    count_lesson = SerializerMethodField()
    lesson = LessonSerializer()

    def get_count_lesson(self, course):
        return Course.objects.filter(lesson=course.lesson).count()

    class Meta:
        model = Course
        fields = ("name", "description", "photo", "count_lesson", "lesson")


