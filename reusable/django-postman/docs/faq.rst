Frequently-asked questions
==========================

General
-------

**I don't want to bother with the moderation feature, how to bypass it?**
    Set the configuration option::

        POSTMAN_AUTO_MODERATE_AS = True

**I installed django-pagination, and still I don't see any pagination widgets**

* Is there really more messages than one page capacity (default is 20)?
* Check that ``pagination`` is declared before ``postman`` in the ``INSTALLED_APPS`` setting.
* See if it's better by disabling :file:`postman/templatetags/pagination_tags.py` and :file:`.pyc` (rename or move the files).
