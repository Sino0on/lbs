from django.urls import path, include
from .views import *


urlpatterns = [
    # path('', include(router.urls)),
    path('calculate/', calculate_sum, name='calculate-sum'),
    path('order/list/', OrderListView.as_view()),
    path('auth/', NewAuthView.as_view()),
    path('register/', UserCreateView.as_view()),
    path('order/create', OrderCreateView.as_view()),
    path('order/create/check/price', CheckPriceView.as_view()),
    path('order/<int:pk>', OrderDetailCreateDeleteView.as_view()),
    path('company/list', CompanyListView.as_view()),
    path('company/create', CompanyCreateView.as_view()),
    path('company/<int:pk>', CompanyDetailCreateDeleteView.as_view()),
    path('feedaback/list', FeedbackListView.as_view()),
    path('feedaback/create', FeedbackCreateView.as_view()),
]
