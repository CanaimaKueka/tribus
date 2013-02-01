Moderation
==========

When created, a message is in a *pending* state. It is not delivered to the recipient
immediately.  By default, some person must review its contents and must either accept
or reject the message.

Moderation is done through the Admin site. To ease the action, a special message type
is available: PendingMessage. It's nothing else but the classic Message type, but:

* It is intended to collect only messages in the *pending* state
* A dedicated simplified change view is available, with two main buttons: Accept and Reject

The moderator can give a reason in case of rejection of the message.
If provided, this piece of information will be reported in the notification to the sender.

Auto moderators
---------------

You may automate the moderation by giving zero, one, or many auto-moderator functions
to the views.  The value of the parameter can be one single function or a sequence of
functions as a tuple or a list.

Views supporting an ``auto-moderators`` parameter are: ``write``, ``reply``.

Example::

    def mod1(message):
        # ...
        return None

    def mod2(message):
        # ...
        return None
    mod2.default_reason = 'mod2 default reason'

    urlpatterns = patterns('postman.views',
        # ...
        url(r'^write/(?:(?P<recipients>[\w.@+-:]+)/)?$', 'write',
            {'auto_moderators': (mod1, mod2)}, name='postman_write'),
        url(r'^reply/(?P<message_id>[\d]+)/$', 'reply',
            {'auto_moderators': mod1}, name='postman_reply'),
        # ...
    )

Each auto-moderator function will be called for the message to moderate,
in the same order as the one set in the parameter.

*Input*:

* ``message``: a Message instance

*Output*:

The structure of the output is either a ``rating`` or a tuple ``(rating, reason)``.

``rating`` may take the following values:

* ``None``
* 0 or ``False``
* 100 or ``True``
* an integer between 1 and 99

``reason`` is a string, giving a specific reason for a rejection.
If not provided, a default reason will be taken from the ``default_reason`` attribute
of the function, if any. Otherwise, there will be no reason.

The processing of the chain of auto-moderators is managed by these rules:

#. If return is ``None`` or outside the range 0..100, the auto-moderator is neutral
#. If return is 0, no other function is processed, the message is rejected
#. If return is 100, no other function is processed, the message is accepted
#. Otherwise, the rating will count for an average among the full set of returned ratings

At the end of the loop, if the decision is not final, the sequence is:

#. If there was no valid rating at all, then the ``POSTMAN_AUTO_MODERATE_AS`` setting applies.
#. An average rating is computed: if greater or equal to 50, the message is accepted.
#. The message is rejected. The final reason is a comma separated collection of reasons
   coming from moderators having returned a rating lesser than 50.


