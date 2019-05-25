from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import OfferViewSet, DiscountViewSet


router = DefaultRouter()
router.register(r'', OfferViewSet, basename='offers')
router.register(r'', DiscountViewSet, base_name='discounts')
urlpatterns = router.urls
