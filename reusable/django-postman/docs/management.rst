Management Commands
===================

postman_cleanup
---------------

When a user deletes a message, the object is not deleted from the database right away,
it is moved to a ``trash`` folder.
One reason is to allow a message to be undeleted if the user wants to retrieve it.
Another reason is that there is only one copy of a message for both the sender and the recipient,
so the message must be marked for deletion by the two parties before to be considered for a withdraw.
An additional constraint is that a message may be a member of a conversation and the reply chain
must be kept consistent.

So there are some criteria to fulfill by a record to be really deleted from the database:

* both the sender and the recipient must have marked the message as deleted
* if the message is in a conversation, all the messages of the conversation must be marked for deletion
* the action of deletion must have been done enough time ago

A management command is provided for this purpose:

:command:`django-admin.py postman_cleanup`

It can be run as a cron job or directly.

The :option:`--days` option can be used to specify the minimal number of days a message/conversation
must have been marked for deletion.
Default value is 30 days.

postman_checkup
---------------

A management command to run a test suite on the messages presently in the database.
It checks messages and conversations for possible inconsistencies, in a read-only mode.
No change is made on the data.

:command:`django-admin.py postman_checkup`

It can be run directly or better as a nightly cron job.
