from django.urls import path

from apps.views.shop import BannerListAPIView, CategoryListAPIView, ProductListAPIView
from apps.views.users import SignInGenericAPIView, UserCreateAPIView

urlpatterns = [
    path('sign-in', SignInGenericAPIView.as_view()),
    path('sign-up', UserCreateAPIView.as_view()),

    path('banners', BannerListAPIView.as_view()),
    path('categories', CategoryListAPIView.as_view()),
    path('products', ProductListAPIView.as_view()),
]
