"""4rent_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from offers.views import (OfferViewSet, DiscountViewSet,
                          CategoryViewSet, FeaturesViewSet, LikeViewSet, StoryViewSet)
from ads.views import AdViewSet
from galleries.views import (
    OfferImageViewSet, DiscountImageViewSet)
from users.views import UserViewSet, AdvertiserNotificationViewSet, SearcherNotificationViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename="users")
router.register('offers', OfferViewSet, basename='offers')
router.register('images-offers', OfferImageViewSet,
                base_name="offers_images")
router.register('images-discounts', DiscountImageViewSet,
                base_name="discounts-images")
router.register('features', FeaturesViewSet, base_name='ad_features')
router.register('discounts', DiscountViewSet, base_name='discounts')
router.register('ads', AdViewSet, base_name='ads')
router.register('categories', CategoryViewSet, base_name="categories")
router.register('likes', LikeViewSet, base_name="likes")
router.register('searchernotifications', SearcherNotificationViewSet, base_name="searcher_notifications")
router.register('advertisernotifications', AdvertiserNotificationViewSet, base_name="advertiser_notifications")
router.register('stories', StoryViewSet, base_name="stories")

urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    path('api/', include(router.urls)),    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
