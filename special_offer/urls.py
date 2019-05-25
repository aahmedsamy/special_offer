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

from offers.views import OfferViewSet, DiscountViewSet


router = DefaultRouter()
router.register(r'api/offers', OfferViewSet, basename='offers')
router.register(r'api/discounts', DiscountViewSet, base_name='discounts')
urlpatterns = router.urls

urlpatterns += (
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    path('api/', include([
        path('users/', include('users.urls')),
    ])),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
