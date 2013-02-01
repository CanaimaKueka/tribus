.. _quickstart:

Quick start guide
=================

Requisites and dependances
--------------------------

Python version >= 2.6

Some reasons:

* use of ``str.format()``

Django version >= 1.2.2

Some reasons:

* use of ``self.stdout`` in management commands

Installation
------------
Get the code from the repository, which is hosted at `Bitbucket <http://bitbucket.org/>`_.

You have two main ways to obtain the latest code and documentation:

With the version control software Mercurial installed, get a local copy by typing::

    hg clone http://bitbucket.org/psam/django-postman/

Or download a copy of the package, which is available in several compressed formats,
either from the ``Download`` tab or from the ``get source`` menu option.

In both case, make sure the directory is accessible from the Python import path.

Configuration
-------------

Required settings
~~~~~~~~~~~~~~~~~

Add ``postman`` to the ``INSTALLED_APPS`` setting of your project.

Run a :command:`manage.py syncdb`

Include the URLconf ``postman.urls`` in your project's root URL configuration.

.. _optional_settings:

Optional settings
~~~~~~~~~~~~~~~~~

If you want to make use of a ``postman_unread_count`` context variable in your templates,
add ``postman.context_processors.inbox`` to the ``TEMPLATE_CONTEXT_PROCESSORS`` setting
of your project.

You may specify some additional configuration options in your :file:`settings.py`:

``POSTMAN_DISALLOW_ANONYMOUS``
    Set it to True if you do not allow visitors to write to users.
    That way, messaging is restricted to a User-to-User exchange.

    *Defaults to*: False.

``POSTMAN_DISALLOW_MULTIRECIPIENTS``
    Set it to True if you do not allow more than one username in the recipient field.

    *Defaults to*: False.

``POSTMAN_DISALLOW_COPIES_ON_REPLY``
    Set it to True if you do not allow additional recipients when replying.

    *Defaults to*: False.

``POSTMAN_DISABLE_USER_EMAILING``
    Set it to True if you do not want basic email notification to users.
    This setting does not apply to visitors (refer to ``POSTMAN_DISALLOW_ANONYMOUS``),
    nor to a notifier application (refer to ``POSTMAN_NOTIFIER_APP``)

    *Defaults to*: False.

``POSTMAN_AUTO_MODERATE_AS``
    The default moderation status when no auto-moderation functions, if any, were decisive.

    * ``True`` to accept messages.
    * ``False`` to reject messages.
    * ``None`` to leave messages to a moderator review.

    *Defaults to*: None.

    To disable the moderation feature (no control, no filter):

    * Set this option to True
    * Do not provide any auto-moderation functions

``POSTMAN_SHOW_USER_AS``
    How to represent a User for display, in message properties: ``obfuscated_recipient`` and ``obfuscated_sender``,
    and in the ``or_me`` filter. The value can be specified as:

    * The name of a property of User. For example: 'last_name'
    * The name of a method of User. For example: 'get_full_name'
    * A function, receiving the User instance as the only parameter. For example: ``lambda u: u.get_profile().nickname``
    * ``None`` : the default text representation of the User (username) is used.

    *Defaults to*: None.

    The default behaviour is used as a fallback when: the value is a string and the result is false
    (misspelled attribute name, empty result, ...), or the value is a function and an exception is raised
    (but any result, even empty, is valid).

``POSTMAN_NOTIFIER_APP``
    A notifier application name, used in preference to the basic emailing,
    to notify users of their rejected or received messages.

    *Defaults to*: 'notification', as in django-notification.

    If you already have a notifier application with the default name in the installed applications
    but you do not want it to be used by this application, set the option to None.

``POSTMAN_MAILER_APP``
    An email application name, used in preference to the basic django.core.mail, to send emails.

    *Defaults to*: 'mailer', as in django-mailer.

    If you already have a mailer application with the default name in the installed applications
    but you do not want it to be used by this application, set the option to None.

``POSTMAN_AUTOCOMPLETER_APP``
    An auto-completer application specification, useful for recipient fields.
    To enable the feature, define a dictionary with these keys:

    * 'name'
        The name of the auto-completer application.
        Defaults to 'ajax_select'
    * 'field'
        The model class name.
        Defaults to 'AutoCompleteField'
    * 'arg_name'
        The name of the argument
        Defaults to 'channel'
    * 'arg_default'
        No default value. This is a mandatory default value, but you may supersede it in the field
        definition of a custom form or pass it in the url pattern definitions.

    *Defaults to*: an empty dictionary.

Templates
~~~~~~~~~
A complete set of working templates is provided with the application.
You may use it as it is with a CSS design of yours, re-use it or extend some parts of it,
or only view it as an example.

You may need to adjust some templates to match your version of Django.
Permute the comment tags for the lines denoted by the marks: {# dj v1.x #} in:

* base_write.html

In case you run a Django 1.2 version, perform these additional steps for any template:

* Remove {% load url from future %}
* Change any {% url 'XX' %} to {% url XX %}

Relations between templates::

    base.html
    |_ base_folder.html
    |  |_ inbox.html
    |  |_ sent.html
    |  |_ archives.html
    |  |_ trash.html
    |_ base_write.html
    |  |_ write.html
    |  |_ reply.html
    |_ view.html

If the autocomplete application is django-ajax-selects in version 1.1.4 or 1.1.5, the following URLs are referenced by this set:

* js/jquery.min.js
* js/jquery.autocomplete.min.js
* css/jquery.autocomplete.css
* css/indicator.gif

You may have to adjust the path prefix with your version of Django:
{{ MEDIA_URL }} or {{ STATIC_URL }} or {% admin_media_prefix %} or {% static '... %} or {% static 'admin/... %}.

These files are part of the requirements of django-ajax-selects version 1.1.x and
it's up to you to make them accessible in your project (they are not provided by the django-postman app).

The :file:`postman/base.html` template extends a :file:`base.html` site template,
in which some blocks are expected:

* title: in <html><head><title>, at least for a part of the entire title string
* extrahead: in <html><head>, to put some <script> and <link> elements
* content: in <html><body>, to put the page contents
* postman_menu: in <html><body>, to put a navigation menu

.. _static files:

Static Files
~~~~~~~~~~~~

A CSS file is provided with the application, for the Admin site: :file:`postman/css/admin.css`.
It is not obligatory but makes the display more confortable.

A basic CSS file is provided to style the views: :file:`postman/css/postman.css`.
You may use it as a starting point to make your own design.

These files are provided under :file:`postman/static/`.

See also :ref:`styles` for the stylesheets of views.

For Django 1.3+, just follow the instructions related to the staticfiles app.

For Django 1.2:
	It's up to you to make the files visible to the URL resolver.

	For example:

	* Rename the path to :file:`postman/medias/`
	* In a production environment, set :file:`/<MEDIA_ROOT>/postman/` as a symlink to :file:`<Postman_module>/medias/postman/`
	* In a development environment (django's runserver), you can put in the URLconf, something like::

		('^' + settings.MEDIA_URL.strip('/') + r'/(?P<path>postman/.*)$', 'django.views.static.serve',
			{'document_root': os.path.join(imp.find_module('postman')[1], 'medias')}),

Examples
--------

:file:`settings.py`::

    INSTALLED_APPS = (
        # 'pagination'  # has to be before postman
        # ...
        'postman',
        # ...
        # 'ajax_select'
        # 'notification'
        # 'mailer'
    )
    # POSTMAN_DISALLOW_ANONYMOUS = True  # default is False
    # POSTMAN_DISALLOW_MULTIRECIPIENTS = True  # default is False
    # POSTMAN_DISALLOW_COPIES_ON_REPLY = True  # default is False
    # POSTMAN_DISABLE_USER_EMAILING = True  # default is False
    # POSTMAN_AUTO_MODERATE_AS = True  # default is None
    # POSTMAN_SHOW_USER_AS = 'get_full_name'  # default is None
    # POSTMAN_NOTIFIER_APP = None  # default is 'notification'
    # POSTMAN_MAILER_APP = None  # default is 'mailer'
    # POSTMAN_AUTOCOMPLETER_APP = {
        # 'name': '',  # default is 'ajax_select'
        # 'field': '',  # default is 'AutoCompleteField'
        # 'arg_name': '',  # default is 'channel'
        # 'arg_default': 'postman_friends',  # no default, mandatory to enable the feature
    # }  # default is {}

:file:`urls.py`::

    (r'^messages/', include('postman.urls')),
