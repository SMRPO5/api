from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'comments', CommentViewSet, base_name='comments')
router.register(r'card_types', CommentViewSet, base_name='card_types')
router.register(r'lanes', CommentViewSet, base_name='lanes')
router.register(r'logged_times', CommentViewSet, base_name='logged_times')
router.register(r'tasks', CommentViewSet, base_name='tasks')
router.register(r'cards', CommentViewSet, base_name='cards')

urlpatterns = [
	url(r'^', include(router.urls))
]
