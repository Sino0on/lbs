from django.urls import path, include
from .views import *


urlpatterns = [
    # path('', include(router.urls)),
    path('calculate/', calculate_sum, name='calculate-sum'),
    path('order/list/', OrderListView.as_view()),
    path('auth/', NewAuthView.as_view()),
    path('register/', UserCreateView.as_view()),
]
