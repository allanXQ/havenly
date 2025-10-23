from rest_framework import routers

router = routers.SimpleRouter()
from .views import OrganizationViewSet, OrganizationRolesViewSet, OrganizationKYCViewSet

router.register(r'organizations', OrganizationViewSet)
router.register(r'organization-roles', OrganizationRolesViewSet)
router.register(r'organization-kyc', OrganizationKYCViewSet)
urlpatterns = router.urls