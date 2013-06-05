Custom views
============

.. _styles:

styles
------
Here is a sample of some CSS rules, usable for :file:`postman/views.html`::

    .pm_message.pm_deleted             { text-decoration: line-through; }
    .pm_message.pm_deleted .pm_body    { display: none; }
    .pm_message.pm_archived            { font-style: italic; color: grey; }
    .pm_message.pm_unread .pm_subject  { font-weight: bolder; }
    .pm_message.pm_pending .pm_header  { background-color: #FFC; }
    .pm_message.pm_rejected .pm_header { background-color: #FDD; }

These rules are provided with the application, as an example, in a static file (See :ref:`static files`).

forms
-----

You can replace the default forms in views.

Examples::

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', 'write',
            {'form_classes': (MyCustomWriteForm, MyCustomAnonymousWriteForm)}, name='postman_write'),
        url(r'^reply/(?P<message_id>[\d]+)/$', 'reply',
            {'form_class': MyCustomFullReplyForm}, name='postman_reply'),
        url(r'^view/(?P<message_id>[\d]+)/$', 'view',
            {'form_class': MyCustomQuickReplyForm}, name='postman_view'),
        # ...
    )

templates
---------

You can replace the default template name in all views.

Example::

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^view/(?P<message_id>[\d]+)/$', 'view',
            {'template_name': 'my_custom_view.html'}, name='postman_view'),
        # ...
    )

after submission
----------------

You can supersede the default view where to return to, after a successful submission.

The default algorithm is:

#. Return where you came from
#. If it cannot be known, fall back to the inbox view
#. But if the submission view has a ``success_url`` parameter, use it preferably
#. In all cases, a ``next`` parameter in the query string has higher precedence

The parameter ``success_url`` is available to these views:

* ``write``
* ``reply``
* ``archive``
* ``delete``
* ``undelete``

Example::

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^reply/(?P<message_id>[\d]+)/$', 'reply',
            {'success_url': 'postman_inbox'}, name='postman_reply'),
        # ...
    )

Example::

    <a href="{% url 'postman_reply' reply_to_pk %}?next={{ next_url|urlencode }}">Reply</a>

reply formatters
----------------

You can replace the default formatters used for replying.

Examples::

    def format_subject(subject):
        return "Re_ " + subject

    def format_body(sender, body):
        return "{0} _ {1}".format(sender, body)

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^reply/(?P<message_id>[\d]+)/$', 'reply',
            {'formatters': (format_subject,format_body)}, name='postman_reply'),
        url(r'^view/(?P<message_id>[\d]+)/$', 'view',
            {'formatters': (format_subject,format_body)}, name='postman_view'),
        # ...
    )
