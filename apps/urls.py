from django.urls import path

from apps.views.selectable import RegionSelectListAPIView, DistrictSelectListAPIView
from apps.views.shop import BannerListAPIView, CategoryListAPIView, ProductListAPIView, FlowCreateAPIView, \
    FlowListAPIView
from apps.views.shop.flow import FlowStatisticsListAPIView
from apps.views.shop.like_product import LikeProductListAPIView, LikeProductCreateAPIView
from apps.views.shop.market_product import MarketProductListAPIView
from apps.views.shop.order import OrderCreateAPIView, OrderListAPIView
from apps.views.shop.product import ProductDetailRetrieveAPIView
from apps.views.shop.request import RequestCreateAPIView, RequestListAPIView
from apps.views.users import SignInGenericAPIView, UserCreateAPIView, BalanceRetrieveAPIView, \
    ConfirmSMSCodeGenericAPIView
from apps.views.users.change_number import UserChangePhoneNumberAPIVIew
from apps.views.users.change_password import UserChangePasswordAPIVIew
from apps.views.users.update import UserUpdateAPIVIew

urlpatterns = [
    path('send-message', ConfirmSMSCodeGenericAPIView.as_view()),
    path('sign-in', SignInGenericAPIView.as_view()),
    path('sign-up', UserCreateAPIView.as_view()),

    path('user-update/<int:pk>', UserUpdateAPIVIew.as_view()),
    path('change-password/<int:pk>', UserChangePasswordAPIVIew.as_view()),
    path('change-number/<int:pk>', UserChangePhoneNumberAPIVIew.as_view()),

    path('balance/<int:pk>', BalanceRetrieveAPIView.as_view()),

    path('request', RequestCreateAPIView.as_view()),
    path('requests', RequestListAPIView.as_view()),

    path('banners', BannerListAPIView.as_view()),
    path('categories', CategoryListAPIView.as_view()),
    path('products', ProductListAPIView.as_view()),
    path('product/<int:pk>', ProductDetailRetrieveAPIView.as_view()),
    path('like-products', LikeProductListAPIView.as_view()),
    path('like-product', LikeProductCreateAPIView.as_view()),

    path('market-products', MarketProductListAPIView.as_view()),

    path('order-create', OrderCreateAPIView.as_view()),
    path('my-orders', OrderListAPIView.as_view()),

    path('flow-create', FlowCreateAPIView.as_view()),
    path('flows', FlowListAPIView.as_view()),
    path('flow-statistics', FlowStatisticsListAPIView.as_view()),

    path('region-select', RegionSelectListAPIView.as_view()),
    path('district-select', DistrictSelectListAPIView.as_view()),
]
