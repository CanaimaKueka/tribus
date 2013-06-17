"""
Views which allow users to create and activate accounts.

"""
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url, render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME, login as django_login, authenticate as django_authenticate
from django.contrib.sites.models import get_current_site
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from tribus.web.auth import signals
from tribus.web.auth.forms import SignupForm, LoginForm
from tribus.web.auth.models import SignupProfile


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
    form_class = SignupForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'auth/signup_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.

        """
        return super(SignupView, self).dispatch(request, *args, **kwargs)

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

        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        new_user = SignupProfile.objects.create_inactive_user(username, email, password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        return ('auth_complete', (), {})


class BaseActivationView(TemplateView):
    """
    Base class for user activation views.

    """
    http_method_names = ['get']
    template_name = 'auth/activate_form.html'

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
        return super(ActivationView, self).get(request, *args, **kwargs)

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
            signals.user_activated.send(sender=self.__class__,
                                        user=activated_user,
                                        request=request)
        return activated_user

    def get_success_url(self, request, user):
        return ('auth_activate_complete', (), {})


# @sensitive_post_parameters()
@csrf_protect
@never_cache
def LoginView(request, template_name='auth/login.html',
              redirect_field_name=REDIRECT_FIELD_NAME,
              authentication_form=LoginForm,
              current_app=None, extra_context=None):

    """
    Displays the login form and handles the login action.
    """

    def HandleResponse(request, form, redirect_to, error_title=None, extra_context=None):
        form.fields['username'].widget.attrs = {
            'placeholder': 'Enter your username',
            'class': 'input-xlarge',
            'label': '',
        }
        form.fields['password'].widget.attrs = {
            'placeholder': 'Enter your password',
            'class': 'input-xlarge'
        }
        form.fields['username'].label = ''
        form.fields['password'].label = ''
        form.fields['remember_me'].label = 'Remember my session'

        current_site = get_current_site(request)

        context = {
            'form': form,
            'error_title': error_title,
            'redirect_field_name': redirect_to,
            'site': current_site,
            'site_name': current_site.name,
        }

        if extra_context is not None:
            context.update(extra_context)

        return TemplateResponse(request, template_name, context,
                                current_app=current_app)

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        request.session.set_test_cookie()

        form = authentication_form(request=request, data=request.POST)

        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            try:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')

            except KeyError:
                error_title = u'Key error'
                return HandleResponse(request, form, redirect_to, error_title)

            user = django_authenticate(username=username, password=password, request=request)
            print username
            print password
            print user

            # Authentication failed
            if not user:
                error_title = u'invalid login'
                return HandleResponse(request, form, redirect_to, error_title)

            # The user is not active
            if not user.is_active():
                error_title = u'account disabled'
                return HandleResponse(request, form, redirect_to, error_title)

            # If we have 'remember_me' checked, user session
            # will never expire
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)

            # Okay, security check complete. Log the user in.
            django_login(request, form.get_user())

            return HttpResponseRedirect(redirect_to)
        else:
            error_title = u'form is invalid'
            return HandleResponse(request, form, redirect_to, error_title)
    else:
        form = authentication_form(request)
        return HandleResponse(request, form, redirect_to)
