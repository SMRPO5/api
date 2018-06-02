from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, base_name='projects')
router.register(r'comments', CommentViewSet, base_name='comments')
router.register(r'card_types', CardTypeViewSet, base_name='card_types')
router.register(r'boards', BoardViewSet, base_name='boards')
router.register(r'lanes', LaneViewSet, base_name='lanes')
router.register(r'logged_times', LoggedTimeViewSet, base_name='logged_times')
router.register(r'tasks', TaskViewSet, base_name='tasks')
router.register(r'cards', CardViewSet, base_name='cards')
router.register(r'columns', ColumnViewSet, base_name='cards')
router.register(r'wip_violations', WIPViolationViewSet, base_name='wip_violations')
router.register(r'card_history', CardHistoryViewSet, base_name='card_history')
router.register(r'board_update', BoardUpdateViewSet, base_name='board_update')
router.register(r'analytics_lead_time', AnalyticsLeadTimeViewSet, base_name='analytics_lead_time')


urlpatterns = [
	url(r'^', include(router.urls)),
# 	url(r'^card_history/(?P<card_id>\d+)/$', CardHistoryViewSet.as_view({'get': 'list'}))
	url(r'^board_copy/(?P<board_id>\d+)/$', CopyBoardView.as_view({'post': 'create'}))
	]
