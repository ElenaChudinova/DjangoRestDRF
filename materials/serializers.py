from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, source="courses")
    count_lesson = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, obj):
        return obj.courses.count()

    def get_lessons(self, course):
        return [lesson.name for lesson in Lesson.objects.filter(course=course)]



class CourseDetailSerializer(ModelSerializer):
    count_lesson = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, obj):
        return obj.courses.count()

