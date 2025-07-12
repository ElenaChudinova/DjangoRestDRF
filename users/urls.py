from django.urls import include, path
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentDestroyAPIView,
                         PaymentListAPIView, PaymentRetrieveAPIView,
                         PaymentUpdateAPIView, UserCreateAPIView, UserViewSet)

app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path(
        "payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment_retrieve"
    ),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path(
        "payment/<int:pk>/delete",
        PaymentDestroyAPIView.as_view(),
        name="payment_delete",
    ),
    path(
        "payment/<int:pk>/update/",
        PaymentUpdateAPIView.as_view(),
        name="payment_update",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("register/", UserCreateAPIView.as_view(), name="register"),
]
