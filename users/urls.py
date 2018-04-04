from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MeViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
router.register(r'me', MeViewSet, base_name='me')

urlpatterns = [
	url(r'^', include(router.urls))
]