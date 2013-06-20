"""
Forms and validation code for user registration.

Note that all of these forms assume Django's bundle default ``User``
model; since it's not possible for a form to anticipate in advance the
needs of custom user models, you will need to write your own forms if
you're using a custom model.

"""


from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import Form
from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(AuthenticationForm):
    """
    Subclass of Django ``AuthenticationForm`` which adds a remember me
    checkbox.
    """

    username = forms.RegexField(
                                    label = _('Username:'), required = True,
                                    regex = r'^[\w.@+-]+$',
                                    widget = forms.TextInput(
                                        attrs= {
                                            'placeholder': _('Enter your username'),
                                            'class': 'input-xlarge'
                                        }
                                    ),
                                    max_length = 30,
                                    error_messages = {
                                        'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
                                    }
                                )

    password = forms.CharField(
                                    label = _('Password:'), required = True,
                                    widget = forms.PasswordInput(
                                        attrs = {
                                            'placeholder': _('Enter your password'),
                                            'class': 'input-xlarge'
                                        }
                                    )
                                )

    remember_me = forms.BooleanField(
                                        label = _('Remember my session'),
                                        initial = False,
                                        required = False
                                    )


class SignupForm(Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    username = forms.RegexField(
                                    label = '', required = True,
                                    regex = r'^[\w.@+-]+$',
                                    widget = forms.TextInput(
                                        attrs= {
                                            'placeholder': _('Pick a username'),
                                            'class': 'input-xlarge'
                                        }
                                    ),
                                    max_length = 30,
                                    error_messages = {
                                    'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")
                                    }
                                )

    email = forms.EmailField(
                                label = '', required = True,
                                widget = forms.TextInput(
                                    attrs = {
                                        'placeholder': _('Enter a valid email'),
                                        'class': 'input-xlarge'
                                    }
                                )
                            )

    password1 = forms.CharField(
                                    label = '', required = True,
                                    widget = forms.PasswordInput(
                                        attrs = {
                                            'placeholder': _('Create a password'),
                                            'class': 'input-xlarge'
                                        }
                                    )
                                )

    password2 = forms.CharField(
                                    label = '', required = True,
                                    widget = forms.PasswordInput(
                                        attrs = {
                                            'placeholder': _('Repeat the password'),
                                            'class': 'input-xlarge'
                                        }
                                    )
                                )

    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
