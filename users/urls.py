from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = router.urls
urlpatterns += (
)