from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from .views import OfferViewSet


router = DefaultRouter()
router.register(r'', OfferViewSet, basename='user')

urlpatterns = router.urls
