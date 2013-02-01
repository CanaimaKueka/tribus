Notification
============

Parties should be notified of these events:

* when a message is rejected (sender)
* when a message or a reply is received (recipient)

.. _for_visitors:

For visitors
------------
An email is sent, using these templates:

* :file:`postman/email_visitor_subject.txt` for the subject
* :file:`postman/email_visitor.txt` for the body

The available context variables are:

* ``site``: the Site instance
* ``object``: the Message instance
* ``action``: 'rejection' or 'acceptance'

Default templates are provided with the application. Same as for the views, you can override them,
and design yours.

For users
---------
Special case: In case of a rejection by the auto moderation feature, the user is immediately aware of it,
so there is no need for a notification in addition.

If a notifier application is configured (see :ref:`optional_settings`), the following labels are used:

* ``postman_rejection`` to notify the sender of the rejection
* ``postman_message`` to notify the recipient of the reception of a message
* ``postman_reply`` to notify the recipient of the reception of a reply

Some extra context variables are passed in the call to the notifier application
and so are available in the templates:

* ``pm_message``: the Message instance
* ``pm_action``: 'rejection' or 'acceptance'

If no notifier application is used, an email is sent, using these templates:

* :file:`postman/email_user_subject.txt` for the subject
* :file:`postman/email_user.txt` for the body

In that case, the information about context variables and templates is the same
as in the :ref:`for_visitors` section above.
