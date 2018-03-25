from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'comments', CommentViewSet, base_name='comments')
router.register(r'card_types', CardTypeViewSet, base_name='card_types')
router.register(r'lanes', LaneViewSet, base_name='lanes')
router.register(r'logged_times', LoggedTimeViewSet, base_name='logged_times')
router.register(r'tasks', TaskViewSet, base_name='tasks')
router.register(r'cards', CardTypeViewSet, base_name='cards')

urlpatterns = [
	url(r'^', include(router.urls))
]
