import re
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from askbot.conf import settings as askbot_settings
from askbot.utils.slug import slugify
from askbot.utils.functions import split_list
from askbot import const
from longerusername import MAX_USERNAME_LENGTH
import logging
import urllib

DEFAULT_NEXT = '/' + getattr(settings, 'ASKBOT_URL')
def clean_next(next, default = None):
    if next is None or not next.startswith('/'):
        if default:
            return default
        else:
            return DEFAULT_NEXT
    if isinstance(next, str):
        next = unicode(urllib.unquote(next), 'utf-8', 'replace')
    next = next.strip()
    logging.debug('next url is %s' % next)
    return next

def get_next_url(request, default = None):
    return clean_next(request.REQUEST.get('next'), default)

def get_db_object_or_404(params):
    """a utility function that returns an object
    in return to the model_name and object_id

    only specific models are accessible
    """
    from askbot import models
    try:
        model_name = params['model_name']
        assert(model_name=='Group')
        model = models.get_model(model_name)
        obj_id = forms.IntegerField().clean(params['object_id'])
        return get_object_or_404(model, id=obj_id)
    except Exception:
        #need catch-all b/c of the nature of the function
        raise Http404

def format_errors(error_list):
    """If there is only one error - returns a string
    corresponding to that error, to remove the <ul> tag.

    If there is > 1 error - then convert the error_list into
    a string.
    """
    if len(error_list) == 1:
        return unicode(error_list[0])
    else:
        return unicode(error_list)

class StrippedNonEmptyCharField(forms.CharField):
    def clean(self, value):
        value = value.strip()
        if self.required and value == '':
            raise forms.ValidationError(_('this field is required'))
        return value

class NextUrlField(forms.CharField):
    def __init__(self):
        super(
            NextUrlField,
            self
        ).__init__(
            max_length = 255,
            widget = forms.HiddenInput(),
            required = False
        )
    def clean(self,value):
        return clean_next(value)

login_form_widget_attrs = { 'class': 'required login' }

class UserNameField(StrippedNonEmptyCharField):
    RESERVED_NAMES = (u'fuck', u'shit', u'ass', u'sex', u'add',
                       u'edit', u'save', u'delete', u'manage', u'update', 'remove', 'new')
    def __init__(
        self,
        db_model=User,
        db_field='username',
        must_exist=False,
        skip_clean=False,
        label=_('Choose a screen name'),
        widget_attrs=None,
        **kw
    ):
        self.must_exist = must_exist
        self.skip_clean = skip_clean
        self.db_model = db_model 
        self.db_field = db_field
        self.user_instance = None
        error_messages={
            'required': _('user name is required'),
            'taken': _('sorry, this name is taken, please choose another'),
            'forbidden': _('sorry, this name is not allowed, please choose another'),
            'missing': _('sorry, there is no user with this name'),
            'multiple-taken': _('sorry, we have a serious error - user name is taken by several users'),
            'invalid': _('user name can only consist of letters, empty space and underscore'),
            'meaningless': _('please use at least some alphabetic characters in the user name'),
            'noemail': _('symbol "@" is not allowed')
        }
        if 'error_messages' in kw:
            error_messages.update(kw['error_messages'])
            del kw['error_messages']

        if widget_attrs:
            widget_attrs.update(login_form_widget_attrs)
        else:
            widget_attrs = login_form_widget_attrs

        max_length = MAX_USERNAME_LENGTH()
        super(UserNameField,self).__init__(
                max_length=max_length,
                widget=forms.TextInput(attrs=widget_attrs),
                label=label,
                error_messages=error_messages,
                **kw
            )

    def clean(self,username):
        """ validate username """
        if self.skip_clean == True:
            logging.debug('username accepted with no validation')
            return username
        if self.user_instance is None:
            pass
        elif isinstance(self.user_instance, User):
            if username == self.user_instance.username:
                logging.debug('username valid')
                return username
        else:
            raise TypeError('user instance must be of type User')

        try:
            username = super(UserNameField, self).clean(username)
        except forms.ValidationError:
            raise forms.ValidationError(self.error_messages['required'])

        username_re_string = const.USERNAME_REGEX_STRING
        #attention: here we check @ symbol in two places: input and the regex
        if askbot_settings.ALLOW_EMAIL_ADDRESS_IN_USERNAME is False:
            if '@' in username:
                raise forms.ValidationError(self.error_messages['noemail'])

            username_re_string = username_re_string.replace('@', '')

        username_regex = re.compile(username_re_string, re.UNICODE)

        if self.required and not username_regex.search(username):
            raise forms.ValidationError(self.error_messages['invalid'])
        if username in self.RESERVED_NAMES:
            raise forms.ValidationError(self.error_messages['forbidden'])
        if slugify(username) == '':
            raise forms.ValidationError(self.error_messages['meaningless'])
        try:
            user = self.db_model.objects.get(
                    **{'%s' % self.db_field : username}
            )
            if user:
                if self.must_exist:
                    logging.debug('user exists and name accepted b/c here we validate existing user')
                    return username
                else:
                    raise forms.ValidationError(self.error_messages['taken'])
        except self.db_model.DoesNotExist:
            if self.must_exist:
                logging.debug('user must exist, so raising the error')
                raise forms.ValidationError(self.error_messages['missing'])
            else:
                logging.debug('user name valid!')
                return username
        except self.db_model.MultipleObjectsReturned:
            logging.debug('error - user with this name already exists')
            raise forms.ValidationError(self.error_messages['multiple-taken'])


def email_is_allowed(
    email, allowed_emails='', allowed_email_domains=''
):
    """True, if email address is pre-approved or matches a allowed
    domain"""
    if allowed_emails:
        email_list = split_list(allowed_emails)
        allowed_emails = ' ' + ' '.join(email_list) + ' '
        email_match_re = re.compile(r'\s%s\s' % email)
        if email_match_re.search(allowed_emails):
            return True

    if allowed_email_domains:
        email_domain = email.split('@')[1]
        domain_list = split_list(allowed_email_domains)
        domain_match_re = re.compile(r'\s%s\s' % email_domain)
        allowed_email_domains = ' ' + ' '.join(domain_list) + ' '
        return domain_match_re.search(allowed_email_domains)

    return False

class UserEmailField(forms.EmailField):
    def __init__(self, skip_clean=False, **kw):
        self.skip_clean = skip_clean

        hidden = kw.pop('hidden', False)
        if hidden is True:
            widget_class = forms.HiddenInput
        else:
            widget_class = forms.TextInput

        super(UserEmailField,self).__init__(
            widget=widget_class(
                    attrs=dict(login_form_widget_attrs, maxlength=200)
                ),
            label=mark_safe(_('Your email <i>(never shared)</i>')),
            error_messages={
                'required':_('email address is required'),
                'invalid':_('please enter a valid email address'),
                'taken':_('this email is already used by someone else, please choose another'),
                'unauthorized':_('this email address is not authorized')
            },
            **kw
        )

    def clean(self, email):
        """ validate if email exist in database
        from legacy register
        return: raise error if it exist """
        email = super(UserEmailField,self).clean(email.strip())
        if self.skip_clean:
            return email
        
        allowed_domains = askbot_settings.ALLOWED_EMAIL_DOMAINS.strip()
        allowed_emails = askbot_settings.ALLOWED_EMAILS.strip()

        if allowed_emails or allowed_domains:
            if not email_is_allowed(
                    email,
                    allowed_emails=allowed_emails,
                    allowed_email_domains=allowed_domains
                ):
                raise forms.ValidationError(self.error_messages['unauthorized'])

        try:
            user = User.objects.get(email__iexact=email)
            logging.debug('email taken')
            raise forms.ValidationError(self.error_messages['taken'])
        except User.DoesNotExist:
            logging.debug('email valid')
            return email
        except User.MultipleObjectsReturned:
            logging.critical('email taken many times over')
            raise forms.ValidationError(self.error_messages['taken'])

class SetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=login_form_widget_attrs),
                                label=_('Password'),
                                error_messages={'required':_('password is required')},
                                )
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=login_form_widget_attrs),
                                label=mark_safe(_('Password <i>(please retype)</i>')),
                                error_messages={'required':_('please, retype your password'),
                                                'nomatch':_('sorry, entered passwords did not match, please try again')},
                                )

    def __init__(self, data=None, user=None, *args, **kwargs):
        super(SetPasswordForm, self).__init__(data, *args, **kwargs)

    def clean_password2(self):
        """
        Validates that the two password inputs match.
        
        """
        if 'password1' in self.cleaned_data:
            if self.cleaned_data['password1'] == self.cleaned_data['password2']:
                self.password = self.cleaned_data['password2']
                self.cleaned_data['password'] = self.cleaned_data['password2']
                return self.cleaned_data['password2']
            else:
                del self.cleaned_data['password2']
                raise forms.ValidationError(self.fields['password2'].error_messages['nomatch'])
        else:
            return self.cleaned_data['password2']

