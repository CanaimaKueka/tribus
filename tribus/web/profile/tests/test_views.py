# import os
# from django.test import Client
# from django.test import TestCase
# from doctest import DocTestSuite
# from django.core.urlresolvers import reverse
# from tribus.web.profile.views import *
# from django.contrib.auth.models import User


# class TestViews(TestCase):

# 	def setUp(self):
# 		self.client = Client()
#         # self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#         # self.user.save()

# 	def test_UserProfile_redirect(self):
# 		response = self.client.get(reverse('userprofile1') )
# 		self.assertEqual(response.status_code, 302)

# 	# def test_UserProfile(self):
# 	# 	self.client.login(username ='homero',password='654321')
# 	# 	response = self.client.get(reverse('userprofile1'))
# 	# 	self.assertEqual(response.status_code, 302)

# 	def test_SearchProfile(self):
# 		response = self.client.post(reverse('registration_login'),{ 'username':'homero', 'password':'23456'})
# 		# self.assertEqual(User.objects., 200)


# 		# response = self.client.get('/profile/homero')
# 		# self.assertEqual(response.status_code, 200)		








