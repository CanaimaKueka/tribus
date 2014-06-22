# import datetime
# import re

# from django.conf import settings
# from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
# from django.core import mail
# from django.core import management
# from django.test import TestCase
# from django.utils.hashcompat import sha_constructor


# class RegistrationModelTests(TestCase):
#     """
#     Test the model and manager used in the default backend.
#     """
#     user_info = {'username': 'alice',
#                  'password': 'swordfish',
#                  'email': 'alice@example.com'}

#     def setUp(self):
#         self.old_activation = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', None)
#         settings.ACCOUNT_ACTIVATION_DAYS = 7


#     def tearDown(self):
#         settings.ACCOUNT_ACTIVATION_DAYS = self.old_activation


#     def test_profile_creation(self):
#         """
#         Creating a registration profile for a user populates the
#         profile with the correct user and a SHA1 hash to use as
#         activation key.

#         """
#         new_user = User.objects.create_user(**self.user_info)
#         profile = RegistrationProfile.objects.create_profile(new_user)

#         self.assertEqual(RegistrationProfile.objects.count(), 1)
#         self.assertEqual(profile.user.id, new_user.id)
#         self.failUnless(re.match('^[a-f0-9]{40}$', profile.activation_key))
#         self.assertEqual(unicode(profile),
#                          "Registration information for alice")


#     def test_activation_email(self):
#         """
#         ``RegistrationProfile.send_activation_email`` sends an
#         email.

#         """
#         new_user = User.objects.create_user(**self.user_info)
#         profile = RegistrationProfile.objects.create_profile(new_user)
#         profile.send_activation_email(Site.objects.get_current())
#         self.assertEqual(len(mail.outbox), 1)
#         self.assertEqual(mail.outbox[0].to, [self.user_info['email']])
