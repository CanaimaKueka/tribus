.. django-postman documentation master file, created by
   sphinx-quickstart on Fri Nov 26 09:32:49 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-postman's documentation!
==========================================

This is an application for `Django <http://www.djangoproject.com>`_-powered websites.

Basically, the purpose is to allow authenticated users of a site to exchange private **messages**
within the site.  In this documentation, the word *user* is to be understood as an instance of a User,
in the django.contrib.auth context.

So it is mainly for a User-to-User exchange.
But it may be beneficial for a subscriber to receive inquiries from any visitor, ie even if non authenticated.
For instance, a subscriber as a service provider wants an ask-me-details form on a presentation page
to facilitate possible business contacts.
In this case, the visitor is presented a compose message form with an additional field to give
an email address for the reply. The email is obfuscated to the recipient.

What is a message ? Roughly a piece of text, about a subject, sent by a sender to a recipient.
Each user has access to a collection of messages, stored in folders:

    | **Inbox** for incoming messages
    | **Sent** for sent messages
    | **Archives** for archived messages
    | **Trash** for messages marked as deleted

In folders, messages can be presented in two modes:

* by **conversation**, for a compact view: the original message and its replies are grouped in a set
  to constitute one sole entry.
  The lastest message (based on the time) is the representative of the set.
* by **message**, for an expanded view: each message is considered by itself.

Here is a summary of features:

* A non-User (email is undisclosed) can write to a User and get a reply
  (can be disabled by configuration)
* Exchanges can be moderated (with auto-accept and auto-reject plug-ins)
* Optional recipient filter plug-ins
* Optional exchange filtering plug-ins (blacklists)
* Multi-recipient writing is possible (can be disabled by configuration)
  with min/max constraints
* Messages are managed by conversations
* Messages in folders are sortable by sender|recipient|subject|date
* 'Archives' folder in addition to classic Inbox, Sent and Trash folders
* A Quick-Reply form to only ask for a response text
* A cleanup management command to clear the old deleted messages

It has support for optional additional applications:

* Autocomplete recipient field (default is 'django-ajax-selects'),
  with multiple recipient management
* New message notification (default is `django-notification`_)
* Asynchronous mailer (default is `django-mailer`_)

.. _`django-notification`: http://github.com/jtauber/django-notification/
.. _`django-mailer`: http://github.com/jtauber/django-mailer/

Moderation
----------
As an option, messages may need to be validated by a moderator before to be visible
to the recipient.  Possible usages are:

* to control there is no unwanted words in the text fields.
* to make sure that no direct contact informations are exchanged when the site is an intermediary
  and delivers services based on subscription fees.

Messages are first created in a *pending* state. A moderator is in charge to change them to
a *rejected* or *accepted* state.  This operation can be done in two ways:

* By a person, through the Admin site. A specially simplified change view is provided,
  with one-click buttons to accept or reject the message.
* Automatically, through one or more auto-moderator functions.

Filters
-------
As options, custom filters can disallow messages, in two ways:

* **user filter**: a user is not in a state to act as a recipient
* **exchange filter**: criteria for a message between a specific sender
  and a specific recipient are not fulfilled

----

Contents:

.. toctree::
   :maxdepth: 2

   quickstart
   moderation
   notification
   views
   features
   tags-filters
   management
   api
   faq

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

