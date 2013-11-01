"""
Views which allow users to create and activate accounts.

"""
import base64
import hashlib
import random
import string

from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.sites.models import get_current_site
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site
from django.contrib.auth.hashers import make_password

from tribus.web.user import signals
from tribus.web.user.forms import SignupForm, LoginForm
from tribus.web.user.models import SignupProfile
from tribus.web.user.pipeline import create_ldap_user



class _RequestPassingFormView(FormView):
    """
    A version of FormView which passes extra arguments to certain
    methods, notably passing the HTTP request nearly everywhere, to
    enable finer-grained processing.
    """
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))



    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(_RequestPassingFormView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(_RequestPassingFormView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(_RequestPassingFormView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        # We need to be able to use the request and the new user when
        # constructing success_url.
        return super(_RequestPassingFormView, self).get_success_url()

    def form_valid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_invalid(form)


class BaseSignupView(_RequestPassingFormView):
    """
    Base class for user registration views.
    """
    disallowed_url = 'registration_disallowed'
    form_class = SignupForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'user/signup_form.html'


    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        
        """
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(BaseSignupView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        success_url = self.get_success_url(request, new_user)

        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = success_url
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(success_url)

    def registration_allowed(self, request):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.
        
        """
        return True

    def register(self, request, **cleaned_data):
        """
        Implement user-registration logic here. Access to both the
        request and the full cleaned_data of the registration form is
        available here.
        
        """
        raise NotImplementedError


class SignupView(BaseSignupView):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.SignupProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.

    """
    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.SignupProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``SignupProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``SignupProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        new_user = SignupProfile.objects.create_inactive_user(
            cleaned_data['username'], cleaned_data['first_name'],
            cleaned_data['last_name'], cleaned_data['email'],
            cleaned_data['password'], site)

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        return ('user_signup_complete', (), {})


class BaseActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    http_method_names = ['get']
    template_name = 'user/activate_form.html'

    def get(self, request, *args, **kwargs):
        activated_user = self.activate(request, *args, **kwargs)
        if activated_user:
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
            success_url = self.get_success_url(request, activated_user)
            try:
                to, args, kwargs = success_url
                return redirect(to, *args, **kwargs)
            except ValueError:
                return redirect(success_url)
        return super(BaseActivationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BaseActivationView, self).get_context_data(**kwargs)
        return context

    def activate(self, request, *args, **kwargs):
        """
        Implement account-activation logic here.

        """
        raise NotImplementedError

    def get_success_url(self, request, user):
        raise NotImplementedError


class ActivationView(BaseActivationView):
    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.

        """
        activated_user = SignupProfile.objects.activate_user(activation_key)

        if activated_user:
            
            ldapuser = create_ldap_user(activated_user)
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):
        return ('user_activate_complete', (), {})


@sensitive_post_parameters()
@csrf_protect
@never_cache
def LoginView(request, template_name='user/login_form.html',
              redirect_field_name=REDIRECT_FIELD_NAME,
              authentication_form=LoginForm,
              current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """

    def HandleResponse(request, form, redirect_to, error_title=None, extra_context=None):

        current_site = get_current_site(request)

        render_css = ['normalize', 'fonts', 'bootstrap', 'bootstrap-responsive',
                        'font-awesome', 'tribus', 'tribus-responsive']

        render_js = ['jquery', 'bootstrap']

        context = {
            'form': form,
            'error_title': error_title,
            'redirect_field_name': redirect_to,
            'site': current_site,
            'site_name': current_site.name,
            'render_js': render_js,
            'render_css': render_css,
        }

        if extra_context is not None:
            extra_context ['render_css']= render_css
            extra_context ['render_js'] = render_js
            
            context.update(extra_context)

        return TemplateResponse(request, template_name, context,
                                current_app=current_app)

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        request.session.set_test_cookie()

        form = authentication_form(request=request, data=request.POST)

        # form.is_valid() validates the user input and also authenticates against
        # the authetication backend. If succeeds, it stores the user object
        # in form.user_cache (called by form.get_user()), so we don't need to
        # authenticate manually
        if form.is_valid():

            # Obtain authenticated user
            if form.user_cache.is_authenticated():

                # If we have 'remember_me' checked, user session
                # will never expire
                if not request.POST.get('remember_me', None):
                    request.session.set_expiry(0)

                # Okay, security check complete. Log the user in.
                login(request, form.get_user())

                # Ensure the user-originating redirection url is safe.
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

                return HttpResponseRedirect(redirect_to)

            else:
                error_title = u'Authentication error'
                return HandleResponse(request, form, redirect_to, error_title)
        else:
            error_title = u'Data is invalid'
            return HandleResponse(request, form, redirect_to, error_title)
    else:
        form = authentication_form(request)
        return HandleResponse(request, form, redirect_to)

