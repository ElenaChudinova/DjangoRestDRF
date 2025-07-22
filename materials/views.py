from django.contrib.admin import action
from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from yaml import serialize

from materials.models import Course, Lesson
from materials.paginators import CustomPagination
from materials.serializers import (
    CourseDetailSerializer,
    CourseSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from materials.tasks import send_inform_about_update_course
from users.models import Subscription
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action in "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    @action
    def update(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if course.update.filter(pk=request.user.pk).exists():
            course.update.remove(request.user)
        else:
            course.update.add(request.user)
            send_inform_about_update_course.delay(course.owner.email)
        serializer = self.get_serializer(course)
        return Response(data=serializer.data)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        ~IsModer,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )
    pagination_class = CustomPagination


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner | ~IsModer,
    )


class SubscriptionAPIView(APIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("sub_course")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(sub_user=user, sub_course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = "подписка удалена"
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(sub_user=user, sub_course=course_item)
            message = "подписка добавлена"
        # Возвращаем ответ в API
        return Response({"message": message})
