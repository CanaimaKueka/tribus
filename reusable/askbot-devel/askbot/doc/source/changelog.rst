Changes in Askbot
=================

Development version
-------------------
* Added backend support for the tag synonyms
* Added management command `apply_hinted_tags` to batch-apply tags from a list
* Added hovercard on the user's karma display in the header
* Added option to hide ad blocks from logged in users
* Applied Askbot templates to the settings control panel
* Added option to auto-follow questions by the question posters with default "on"
* Support for Django 1.5
* Auto-tweet option for questions and answers
* Added Chech and Croatian translations
* Disable/enable best answer feature
* Allowed post owners repost answers and comments (this used to be mod-only function).
* Answer editor is "folded" by default. Editor buttons and options show on click.
* Management command `askbot_import_jive` to import data from Jive forums.
* Added possibility to choose editor for comments: plain text, or same as
  editor used for the questions or answers: WMD or TinyMCE.
* Added ajax search to the tags page
* Added a placeholder template for the custom javascript on the question page
* Allowed to disable the big "ask" button.
* Some support for the media compression (Tyler Mandry)
* Allowed to enable and disable question scopes on the main page
* Added full text support for some languages with Postgresql:
  Danish, Dutch, English, Finnish, French, German, Hungarian,
  Italian, Japanese (requires package textsearch_ja), Norwegian,
  Portugese, Romanian, Russian, Spanish, Swedish, Turkish.
* repost answer as a comment under the previous (older) answer
* minor edit option for question and answer, to suppress email alerts
* allowed tags to be created upon marking them as interesting/ignored/subscribed

0.7.48 (Jan 28, 2013)
---------------------
* made "how to ask the question" instructions editable
* added RSS auto-discovery link
* added support for multilingual site (experimental)
* tag subscription manager on the tags page (Adolfo)

0.7.47 (Dec 13, 2012)
---------------------
* Bugfix release

0.7.46 (Dec 12, 2012)
---------------------
* Bugfix release

0.7.45 (Dec 12, 2012)
---------------------
* Feedback sender's email is added to the Reply-To header
  in the feedback form (Evgeny)
* Reimplemented search as drop-down (Evgeny)
* Basic design to work on smartphones (Evgeny)
* Allowed use of alternative form on the user signup page (Evgeny)

0.7.44 (Nov 11, 2012)
---------------------
* Support for django 1.4 (Adolfo)
* Added option to enable/disable rss feeds (Evgeny)
* Added minimum reputation to insert links and hotlinked images (Evgeny)
* Added minimum reputation to suggest links as plain text (Evgeny)
* Added support of Haystack for search (Adolfo)
* Added minimum reputation setting to accept any answer as correct (Evgeny)
* Added "VIP" option to groups - if checked, all posts belong to the group and users of that group in the future will be able to moderate those posts. Moderation features for VIP group are in progress (Evgeny)
* Added setting `NOTIFICATION_DELAY_TIME` to use with enabled celery daemon (Adolfo)
* Added setting `ASKBOT_INTERNAL_IPS` - to allow anonymous access to 
  closed sites from dedicated IP addresses (Evgeny)
* Moved default skin from `askbot/skins/default` to simply `askbot` (Evgeny)
* Repost comment as answer (Adolfo)
* Question list widget (Adolfo)
* Ask a question widget (Adolfo)
* Embeddable widget generator (Adolfo)
* Groups are shown in the dropdown menu in the header (Adolfo)
* Added group moderation requests to the moderators inboxes (Evgeny)
* Group joining may be open/closed or moderated (Evgeny)
* Adding "extra options" to the ldap session (Evgeny)
* Tag moderation (Evgeny)
* Editable optional three level category selector for the tags (Evgeny)
* Tag editor adding tags as they are typed (Evgeny)
* Added optional support for unicode slugs (Evgeny)
* Allow switching comment with answer and answer with question comment (Adolfo)
* Allow user names longer than 30 characters (Evgeny)
* Option to disable feedback form for the anonymos users (Evgeny)
* Optional restriction to have confirmed email address to join forum (Evgeny)
* Optional list of allowed email addresses and email domain name for the new users (Evgeny)
* Optional support for unicode slugs (Evgeny)
* Optionally allow limiting one answer per question per person (Evgeny)
* Added management command `build_livesettings_cache` (Adolfo)
* Administrators can post under fictional user accounts without logging out (jtrain, Evgeny)
* Welcome email for the case when replying by email is enabled (Evgeny)
* Detection of email signature based on the response to the welcome email (Evgeny)
* Hide "website" and "about" section of the blocked user profiles
  to help prevent user profile spam (Evgeny)
* Added a function to create a custom user profile tab,
  the feature requires access to the server (Evgeny)
* Added optional top banner to the question page (Evgeny)
* Made "bootstrap mode" default and created instead "large site mode" (Evgeny)
* Added interesting/ignored/subscribed tags to the user profile page (Paul Backhouse, Evgeny)

0.7.43 (May 14, 2012)
---------------------
* User groups (Evgeny)
* Public/Private/Hidden reputation (Evgeny)
* Enabling/disabling the badges system (Evgeny)
* Created a basic post moderation feature (Evgeny)
* Created a way to specify reasons for rejecting posts in a modal dialog (Evgeny)
* A number of bug fixes (Adolfo Fitoria, Jim Tittsler, 
  Evgeny Fadeev, Robin Stocker, Radim Řehůřek, Silvio Heuberger)

0.7.41, 0.7.42 (April 21, 2012)
-------------------------------
* Bug fixes

0.7.40 (March 29, 2012)
-----------------------
* New data models!!! (`Tomasz Zieliński <http://pyconsultant.eu>`_)
* Made email recovery link work when askbot is deployed on subdirectory (Evgeny)
* Added tests for the CSRF_COOKIE_DOMAIN setting in the startup_procedures (Evgeny)
* Askbot now respects django's staticfiles app (Radim Řehůřek, Evgeny)
* Fixed the url translation bug (Evgeny)
* Added left sidebar option (Evgeny)
* Added "help" page and links to in the header and the footer (Evgeny)
* Removed url parameters and the hash fragment from uploaded files -
  amazon S3 for some reason adds weird expiration parameters (Evgeny)
* Reduced memory usage in data migrations (Evgeny)
* Added progress bars to slow data migrations (Evgeny)
* Added a management command to build_thread_summary_cache (Evgeny)
* Added a management delete_contextless_badge_award_activities (Evgeny)
* Fixed a file upload issue in FF and IE found by jerry_gzy (Evgeny)
* Added test on maximum length of title working for utf-8 text (Evgeny)
* Added caching and invalidation to the question page (Evgeny)
* Added a management command delete_contextless_activities (Evgeny)
* LDAP login configuration (github user `monkut <https://github.com/monkut>`_)
* Check order of middleware classes (Daniel Mican)
* Added "reply by email" function (`Vasil Vangelovski <http://www.atomidata.com>`_)
* Enabled "ask by email" via Lamson (Evgeny)
* Tags can be optional (Evgeny)
* Fixed dependency of Django up to 1.3.1, because settings must be upgraded
  for Django 1.4 (Evgeny)

0.7.39 (Jan 11, 2012)
---------------------
* restored facebook login after FB changed the procedure (Evgeny)

0.7.38 (Jan 11, 2012)
---------------------
* xss vulnerability fix, issue found by Radim Řehůřek (Evgeny)

0.7.37 (Jan 8, 2012)
--------------------
* added basic slugification treatment to question titles with 
  ``ALLOW_UNICODE_SLUGS = True`` (Evgeny)
* added verification of the project directory name to
  make sure it does not contain a `.` (dot) symbol (Evgeny)
* made askbot compatible with django's `CSRFViewMiddleware`
  that may be used for other projects (Evgeny)
* added more rigorous test for the user name to make it slug safe (Evgeny)
* made setting `ASKBOT_FILE_UPLOAD_DIR` work (Radim Řehůřek)
* added minimal length of question title ond body
  text to live settings and allowed body-less questions (Radim Řehůřek, Evgeny)
* allowed disabling use of gravatar site-wide (Rosandra Cuello Suñol)
* when internal login app is disabled - links to login/logout/add-remove-login-methods are gone (Evgeny)
* replaced setting `ASKBOT_FILE_UPLOAD_DIR` with django's `MEDIA_ROOT` (Evgeny)
* replaced setting `ASKBOT_UPLOADED_FILES_URL` with django's `MEDIA_URL` (Evgeny)
* allowed changing file storage backend for file uploads by configuration (Evgeny)
* file uploads to amazon S3 now work with proper configuration (Evgeny)

0.7.36 (Dec 20, 2011)
---------------------
* bugfix and made the logo not used by default

0.7.35 (Dec 15, 2011)
---------------------
* Removal of offensive flags (`Dejan Noveski <http://www.atomidata.com/>`_)
* Fixes in CSS (`Byron Corrales <http://byroncorrales.blogspot.com/>`_)
* Update of Catalan locale (Jordi Bofill)

0.7.34 (Dec 10, 2011)
---------------------
* Returned support of Django 1.2

0.7.33 (Dec 6, 2011)
--------------------
* Made on log in redirect to the forum index page by default
  and to the question page, if user was reading the question
  it is still possible to override the ``next`` url parameter
  or just rely on django's ``LOGIN_REDIRECT_URL`` (Evgeny)
* Implemented retraction of offensive flags (Dejan Noveski)
* Made automatic dependency checking more complete (Evgeny)

0.7.32 (Nov 30, 2011)
---------------------
* Bugfixes in English locale (Evgeny)

0.7.31 (Nov 29, 2011)
---------------------
* Added ``askbot_create_test_fixture`` management command (Dejan Noveski)
* Integrated new test fixture into the page load test cases (Dejan Noveski)
* Added an embeddable widget for the questions list matching tags (Daniel Mican, Evgeny Fadeev, Dejan Noveski)

0.7.30 (Nov 28, 2011)
---------------------
Note: some of these features were added in one of the three previous versions.

* Context-sensitive RSS url (`Dejan Noveski <http://www.atomidata.com/>`_)
* Implemented new version of skin (Byron Corrales)
* Show unused vote count (Tomasz Zielinski)
* Categorized live settings (Evgeny)
* Merge users management command (Daniel Mican)
* Added management command ``send_accept_answer_reminders`` (Evgeny)
* Improved the ``askbot-setup`` script (Adolfo, Evgeny)
* Merge users management command (Daniel Mican)
* Anonymous caching of the question page (Vlad Bokov)
* Fixed sharing button bug, css fixes for new template (Alexander Werner)
* Added ASKBOT_TRANSLATE_URL setting for url localization(Alexander Werner)
* Changed javascript translation model, moved from jqueryi18n to django (Rosandra Cuello Suñol)
* Private forum mode (Vlad Bokov)
* Improved text search query in Postgresql (Alexander Werner)
* Take LANGUAGE_CODE from request (Alexander Werner)
* Added support for LOGIN_REDIRECT_URL to the login app (hjwp, Evgeny)
* Updated Italian localization (Luca Ferroni)
* Added Catalan localization (Jordi Bofill)
* Added management command ``askbot_add_test_content`` (Dejan Noveski)
* Continued work on refactoring the database schema (Tomasz Zielinski)

0.7.27 - 0.7.29 (Nov 8-28, 2011)
--------------------------------
For these versions we did not keep consistent record of features.

0.7.26 (Oct 12, 2011)
---------------------
* Added settings for email subscription defaults (Adolfo)
* Resolved `bug #102<http://bugs.askbot.org/issues/102>`_ - duplicate notifications on posts with mentions (Evegeny)
* Added color-animated transitions when urls with hash tags are visited (Adolfo)
* Repository tags will be `automatically added <http://askbot.org/en/question/345/can-git-tags-be-created-for-each-of-the-releases>`_ to new releases (Evgeny, suggsted by ajmirsky)

0.7.25 (Oct 5 2011)
-------------------
* RSS feed for individual question (Sayan Chowdhury)
* Allow pre-population of tags via ask a questions link (Adolfo)
* Make answering own question one click harder (Adolfo)
* Bootstrap mode (Adolfo, Evgeny)
* Color-animated urls with the hash fragments (Adolfo)

0.7.24
------
* Made it possible to disable the anonymous user greeting alltogether (Raghu Udiyar)
* Added annotations for the meanings of user levels on the "moderation" page. (Jishnu)
* Auto-link patterns - e.g. to bug databases - are configurable from settings. (Arun SAG)

0.7.23
------
* Greeting for anonymuos users can be changed from live settings (Hrishi)
* Greeting for anonymous users is shown only once (Rag Sagar)
* Added support for Akismet spam detection service (Adolfo Fitoria)
* Added noscript message (Arun SAG)
* Support for url shortening with TinyUrl on link sharing (Rtnpro)
* Allowed logging in with password and email in the place of login name (Evgeny)
* Added config settings allowing adjust license information (Evgeny)

0.7.22
------
* Media resource revision is now incremented 
  automatically any time when media is updated (Adolfo Fitoria, Evgeny Fadeev)
* First user automatically becomes site administrator (Adolfo Fitoria)
* Avatar displayed on the sidebar can be controlled with livesettings.(Adolfo Fitoria, Evgeny Fadeev)
* Avatar box in the sidebar is ordered with priority for real faces.(Adolfo Fitoria)
* Django's createsuperuser now works with askbot (Adolfo Fitoria)

0.7.21
------
This version was skipped

0.7.20
------
* Added support for login via self-hosted Wordpress site (Adolfo Fitoria)
* Allowed basic markdown in the comments (Adolfo Fitoria)
* Added this changelog (Adolfo Fitoria)
* Added support for threaded emails (Benoit Lavigne)
* A few more Spanish translation strings (Byron Corrales)
* Social sharing support on identi.ca (Rantadeep Debnath)

0.7.19
------
* Changed the Favorite question function for Follow question.
* Fixed issues with page load time.
* Added notify me checkbox to the sidebar.
* Removed MySql dependency from setup.py
* Fixed Facebook login.
* `Fixed "Moderation tab is misaligned" issue reported by methner. <http://askbot.org/en/question/587/moderation-tab-is-misaligned-fixed>`_
* Fixed bug in follow users and changed the follow button design.

0.7.18
------
* `Added multiple capitalization to username mentions(reported by niles) <http://askbot.org/en/question/580/allow-alternate-capitalizations-in-user-links>`_

0.7.17
------
* Adding test for UserNameField.
* Adding test for markup functions.

0.7.16
------
* Admins can add aministrators too.
* Added a postgres driver version check in the start procedures due to a bug in psycopg2 2.4.2.
* New inbox system style (`bug reported by Tomasz P. Szynalski <http://askbot.org/en/question/470/answerscomments-are-listed-twice-in-the-inbox>`_).

0.7.15
------
* Fixed integration with Django 1.1.
* Fixed bugs in setup script.
* Fixed pypi bugs.
