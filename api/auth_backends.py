from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from defender import utils
from defender import config
from django.utils.translation import ugettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions

UserModel = get_user_model()


class DefendedModelBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs):
		if username is None:
			username = kwargs.get(UserModel.USERNAME_FIELD)
			if utils.is_already_locked(request, username=username):
				detail = "You have attempted to login {failure_limit} times, with no success. Your account is locked " \
						 "for {cooloff_time_seconds} seconds".format(failure_limit=config.FAILURE_LIMIT + 1,
																	 cooloff_time_seconds=config.COOLOFF_TIME
				)
				raise exceptions.AuthenticationFailed({'non_field_errors': [_(detail)]})
		user = None
		try:
			user = UserModel._default_manager.get_by_natural_key(username)
		except UserModel.DoesNotExist as e:
			# Run the default password hasher once to reduce the timing
			# difference between an existing and a nonexistent user (#20760).
			UserModel().set_password(password)

		can_login = user and user.check_password(password)

		if can_login:
			login_unsuccessful = False
		else:
			login_unsuccessful = True

		utils.add_login_attempt_to_db(request, login_valid=not login_unsuccessful, username=username)
		user_not_blocked = utils.check_request(request, login_unsuccessful=login_unsuccessful, username=username)

		if user_not_blocked and not login_unsuccessful and can_login:
			return user
