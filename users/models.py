from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.query import QuerySet
from dev_groups.models import Group
import logging

logger = logging.getLogger(__name__)


class EmailUserManager(BaseUserManager):
	"""
	A custom user manager to deal with emails as unique identifiers for auth
	instead of usernames. The default that's used is "UserManager"
	"""
	def _create_user(self, email, password, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('The Email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		""" Create and save an EmailUser with the given email and password.
		:param str email: user email
		:param str password: user password
		:return custom_user.models.EmailUser user: regular user
		"""
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')
		return self._create_user(email, password, **extra_fields)

	def get_queryset(self):
		return EmailQuerySet(self.model, using=self._db)


class EmailQuerySet(QuerySet):
	def filter(self, *args, **kwargs):
		if 'username' in kwargs:
			kwargs.update({'email': kwargs.pop('username')})
		if 'username__in' in kwargs:
			kwargs.update({'email__in': kwargs.pop('username__in')})
		return super(EmailQuerySet, self).filter(*args, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True, null=True)

	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	allowed_roles = models.ManyToManyField(Group, related_name='allowed_users')

	USERNAME_FIELD = 'email'
	objects = EmailUserManager()

	def __str__(self):
		return self.email

	def delete(self, using=None, keep_parents=False):
		self.is_active = False
		self.save()

	@property
	def username(self):
		return self.email
