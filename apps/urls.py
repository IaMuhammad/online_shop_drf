from django.urls import path

from apps.views.shop import BannerListAPIView, CategoryListAPIView, ProductListAPIView, FlowCreateAPIView, \
    FlowListAPIView
from apps.views.shop.flow import FlowStatisticsListAPIView
from apps.views.shop.request import RequestCreateAPIView, RequestListAPIView
from apps.views.users import SignInGenericAPIView, UserCreateAPIView, BalanceRetrieveAPIView, \
    ConfirmSMSCodeGenericAPIView

urlpatterns = [
    path('send-message', ConfirmSMSCodeGenericAPIView.as_view()),
    path('sign-in', SignInGenericAPIView.as_view()),
    path('sign-up', UserCreateAPIView.as_view()),

    path('balance/<int:pk>', BalanceRetrieveAPIView.as_view()),

    path('request', RequestCreateAPIView.as_view()),
    path('requests', RequestListAPIView.as_view()),

    path('banners', BannerListAPIView.as_view()),
    path('categories', CategoryListAPIView.as_view()),
    path('products', ProductListAPIView.as_view()),

    path('flow-create', FlowCreateAPIView.as_view()),
    path('flows', FlowListAPIView.as_view()),
    path('flow-statistics', FlowStatisticsListAPIView.as_view()),
]
