Tags and Filters
================

The following tags and filters are available to your templates by loading the library::

    {% load postman_tags %}

Here are the other special libraries in the :file:`postman/templatetags/` directory,
that are not intended for your site design:

* :file:`postman_admin_modify.py`: a library exclusively designed for a customized change_form
  template used in the Admin site for the moderation of pending messages.

* :file:`pagination_tags.py`: a mock of the django-pagination application template tags.
  For convenience, the design of the default template set is done with the use of that application.
  The mock will avoid failures in template rendering if the real application is not installed,
  as it may be the case for the test suite run in a minimal configuration.
  To deactivate the mock and use the real implementation, just make sure that ``pagination`` is declared
  before ``postman`` in the ``INSTALLED_APPS`` setting.

Tags
----

postman_unread
~~~~~~~~~~~~~~

Gives the number of unread messages for a user.
Returns nothing (an empty string) for anonymous users.

Storing the count in a variable for further processing is advised, such as::

    {% postman_unread as unread_count %}
    ...
    {% if unread_count %}
        You have <strong>{{ unread_count }}</strong> unread messages.
    {% endif %}

postman_order_by
~~~~~~~~~~~~~~~~

Returns a formatted GET query string, usable to have the messages list presented in
a specific order.  This string must be put in the href attribute of a <a> HTML tag.

One argument is required: a keyword to specify the field used for the sort.
Supported values are:

* sender
* recipient
* subject
* date

If the list is already sorted by the keyword, the returned value will specify
the reversed order.  If there are other existing parameters, such as a page number,
they are preserved in the resulting output.

Example::

    <a href="{% postman_order_by subject %}">...</a>

Filters
-------

or_me
~~~~~

If the value is equal to the argument, replace it with the constant string '<me>'.

For example, if we have::

    {{ message.obfuscated_sender|or_me:user }}

and the sender is the currently logged-in user, the output is compacted to show only
the simple pattern '<me>'.

Note that this pattern cannot be confused with the username of a real user,
because the brackets are not in the valid character set for a username.

compact_date
~~~~~~~~~~~~

Output a date as short as possible. The argument must provide three date format patterns.
The pattern used depends on how the date compares to the current instant:

* pattern 1 if in the same day
* pattern 2 if in the same year
* pattern 3 otherwise

For example::

    {{ message.sent_at|compact_date:_("g:i A,M j,n/j/y") }}

With a message sent on "5 dec 2010, 09:21:58":

============  ==============
for the day:  the output is:
============  ==============
5 dec 2010    9:21 AM
6 dec 2010    Dec 5
1 jan 2011    12/5/10
============  ==============
