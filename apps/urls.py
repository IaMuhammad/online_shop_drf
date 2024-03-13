from django.urls import path

from apps.views.shop.banners import BannerListAPIView
from apps.views.users.sign_in import SignInGenericAPIView
from apps.views.users.sign_up import UserCreateAPIView

urlpatterns = [
    path('sign-in', SignInGenericAPIView.as_view()),
    path('sign-up', UserCreateAPIView.as_view()),

    path('banners', BannerListAPIView.as_view()),
]
