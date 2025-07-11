from rest_framework import filters, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserSerializer, PaymentSerializer

from users.models import Payment, User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Разрешение по умолчанию для всех методов

    def get_permissions(self):
        """
        Возвращает список классов разрешений для текущего действия.
        """
        if self.action == 'list' or self.action == 'retrieve':
            # Для методов list и retrieve (GET) применяется IsAuthenticated
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            # Для метода create (POST) применяется IsAuthenticated
            return [permissions.IsAuthenticated()]
        else:
            # Для остальных действий (например, пользовательские действия)
            return [permissions.IsAuthenticated()]


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ('payment_method',)
    ordering_fields = ("date_payment",)


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer