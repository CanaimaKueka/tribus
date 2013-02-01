API
===

For an easier usage of the application from other applications in the project,
an API is provided.

pm_broadcast()
--------------
Broadcast a message to multiple Users.

For an easier cleanup, all these messages are directly marked as archived and deleted on the sender side.
The message is expected to be issued from a trusted application, so moderation
is not necessary and the status is automatically set to 'accepted'.

Arguments: (sender, recipients, subject, body='', skip_notification=False)

pm_write()
----------
Write a message to a User.

Contrary to pm_broadcast(), the message is archived and/or deleted on the sender side only if requested.
The message may come from an untrusted application, a gateway for example,
so it may be useful to involve some auto moderators in the processing.

Arguments: (sender, recipient, subject, body='', skip_notification=False,
auto_archive=False, auto_delete=False, auto_moderators=[])

Arguments
---------
* ``auto_archive``: to mark the message as archived on the sender side
* ``auto_delete``: to mark the message as deleted on the sender side
* ``auto_moderators``: a list of auto-moderation functions
* ``body``: the contents of the message
* ``recipient``: a User instance
* ``recipients``: a list or tuple of User instances, or a single User instance
* ``sender``: a User instance
* ``skip_notification``: if the normal notification event is not wished
* ``subject``: the subject of the message

Example
-------
Suppose an application managing Event objects. Whenever a new Event is generated,
you want to broadcast an announcement to Users who have subscribed
to be informed of the availability of such a kind of Event.

Code sample::

    from postman.api import pm_broadcast
    events = Event.objects.filter(...)
    for e in events:
        pm_broadcast(
            sender=e.author,
            recipients=e.subscribers,
            subject='New {0} at Our School: {1}'.format(e.type, e.title),
            body=e.description)
