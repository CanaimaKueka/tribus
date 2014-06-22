import os
from django.test import Client
from tastypie.test import ResourceTestCase
from doctest import DocTestSuite
from django.core.urlresolvers import reverse
from tribus.web.profile.views import *
from django.contrib.auth.models import User


class EntryResourcesTest(ResourceTestCase):
	"""
		Test para tribus.web.api.autorization.py
	"""
	fixtures = ['test_entries.json']

	def setUp(self):
		super(EntryResourcesTest, self).setUp()

		self.username = 'luis'
		self.password = '123456'
		self.user = User.objects.create_user(self.username, 'example@example.com', self.password)
		









