from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import DevGroupViewSet

router = DefaultRouter()
router.register(r'dev_groups', DevGroupViewSet, base_name='dev_groups')

urlpatterns = [
	url(r'^', include(router.urls))
]