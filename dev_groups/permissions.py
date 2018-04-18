from rest_framework.permissions import BasePermission

KANBAN_MASTER = 'Kanban Master'
MODIFY_METHODS = ['POST', 'PATCH', 'PUT', 'DELETE']


class KanBanMasterCanCreateUpdateDelete(BasePermission):

	def has_permission(self, request, view):
		if request.method in MODIFY_METHODS:
			if request.user.is_kanban_master_allowed() or request.user.is_superuser:
				return True
			else:
				return False
		return True
