from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')

"""
GET, POST
/users/users []

PATCH, PUT, DELETE GET
/users/users/<id

"""

urlpatterns = [
	url(r'^', include(router.urls))
]