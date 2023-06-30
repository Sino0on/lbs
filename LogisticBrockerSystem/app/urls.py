from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'all', AllViewSet, basename='all')
router.register(r'deliverydocs', DeliveryDocsViewSet)
router.register(r'delivery', DeliveryViewSet)
router.register(r'driver', DriverViewSet)
router.register(r'price', PriceViewSet)
router.register(r'driverdocument', DriverDocumentViewSet)
router.register(r'order', OrderViewSet)
router.register(r'user', UserViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'message', MessageViewSet)
router.register(r'messagedoc', MessageDocViewSet)
router.register(r'companyfeedback', CompanyFeedbackViewSet)
router.register(r'feedbackimage', FeedbackImageViewSet)
router.register(r'chat', ChatViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculate/', calculate_sum, name='calculate-sum'),
]
