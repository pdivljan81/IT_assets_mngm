from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from inventory.views import DepartmentViewSet, ITUserViewSet, DeviceViewSet, CredentialReadOnlyViewSet

router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'itusers', ITUserViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'credentials', CredentialReadOnlyViewSet)  # ili CredentialReadOnlyViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
