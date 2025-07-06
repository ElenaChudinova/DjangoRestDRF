from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig

from users.views import UserViewSet, PaymentListAPIView, PaymentRetrieveAPIView, PaymentCreateAPIView, \
    PaymentDestroyAPIView, PaymentUpdateAPIView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("", UserViewSet)


urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_retrieve"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("payment/<int:pk>/delete", PaymentDestroyAPIView.as_view(), name="payment_delete"),
    path("payment/<int:pk>/update/", PaymentUpdateAPIView.as_view(), name="payment_update"),
]

urlpatterns += router.urls