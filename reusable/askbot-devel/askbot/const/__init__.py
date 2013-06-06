# encoding:utf-8
"""
All constants could be used in other modules
For reasons that models, views can't have unicode
text in this project, all unicode text go here.
"""
from django.utils.translation import ugettext_lazy as _
import re

CLOSE_REASONS = (
    (1, _('duplicate question')),
    (2, _('question is off-topic or not relevant')),
    (3, _('too subjective and argumentative')),
    (4, _('not a real question')),
    (5, _('the question is answered, right answer was accepted')),
    (6, _('question is not relevant or outdated')),
    (7, _('question contains offensive or malicious remarks')),
    (8, _('spam or advertising')),
    (9, _('too localized')),
)

LONG_TIME = 60*60*24*30 #30 days is a lot of time
DATETIME_FORMAT = '%I:%M %p, %d %b %Y'

SHARE_NOTHING = 0
SHARE_MY_POSTS = 1
SHARE_EVERYTHING = 2
SOCIAL_SHARING_MODE_CHOICES = (
    (SHARE_NOTHING, _('disable sharing')),
    (SHARE_MY_POSTS, _('my posts')),
    (SHARE_EVERYTHING, _('all posts'))
)

TYPE_REPUTATION = (
    (1, 'gain_by_upvoted'),
    (2, 'gain_by_answer_accepted'),
    (3, 'gain_by_accepting_answer'),
    (4, 'gain_by_downvote_canceled'),
    (5, 'gain_by_canceling_downvote'),
    (-1, 'lose_by_canceling_accepted_answer'),
    (-2, 'lose_by_accepted_answer_cancled'),
    (-3, 'lose_by_downvoted'),
    (-4, 'lose_by_flagged'),
    (-5, 'lose_by_downvoting'),
    (-6, 'lose_by_flagged_lastrevision_3_times'),
    (-7, 'lose_by_flagged_lastrevision_5_times'),
    (-8, 'lose_by_upvote_canceled'),
    #for reputation type 10 Repute.comment field is required
    (10, 'assigned_by_moderator'),
)

#do not translate keys
POST_SORT_METHODS = (
    ('age-desc', _('newest')),
    ('age-asc', _('oldest')),
    ('activity-desc', _('active')),
    ('activity-asc', _('inactive')),
    ('answers-desc', _('hottest')),
    ('answers-asc', _('coldest')),
    ('votes-desc', _('most voted')),
    ('votes-asc', _('least voted')),
    ('relevance-desc', _('relevance')),
)

POST_TYPES = ('answer', 'comment', 'question', 'tag_wiki', 'reject_reason')

SIMPLE_REPLY_SEPARATOR_TEMPLATE = '==== %s -=-=='

#values for SELF_NOTIFY_WHEN... settings use bits
NEVER = 'never'
FOR_FIRST_REVISION = 'first'
FOR_ANY_REVISION = 'any'
SELF_NOTIFY_EMAILED_POST_AUTHOR_WHEN_CHOICES = (
    (NEVER, _('Never')),
    (FOR_FIRST_REVISION, _('When new post is published')),
    (FOR_ANY_REVISION, _('When post is published or revised')),
)
#need more options for web posts b/c user is looking at the page
#when posting. when posts are made by email - user is not looking
#at the site and therefore won't get any feedback unless an email is sent back
#todo: rename INITIAL -> FIRST and make values of type string
#FOR_INITIAL_REVISION_WHEN_APPROVED = 1
#FOR_ANY_REVISION_WHEN_APPROVED = 2
#FOR_INITIAL_REVISION_ALWAYS = 3
#FOR_ANY_REVISION_ALWAYS = 4
#SELF_NOTIFY_WEB_POST_AUTHOR_WHEN_CHOICES = (
#    (NEVER, _('Never')),
#    (
#        FOR_INITIAL_REVISION_WHEN_APPROVED,
#        _('When inital revision is approved by moderator')
#    ),
#    (
#        FOR_ANY_REVISION_WHEN_APPROVED,
#        _('When any revision is approved by moderator')
#    ),
#    (
#        FOR_INITIAL_REVISION_ALWAYS,
#        _('Any time when inital revision is published')
#    ),
#    (
#        FOR_ANY_REVISION_ALWAYS,
#        _('Any time when revision is published')
#    )
#)

REPLY_SEPARATOR_TEMPLATE = '==== %(user_action)s %(instruction)s -=-=='
REPLY_WITH_COMMENT_TEMPLATE = _(
    'Note: to reply with a comment, '
    'please use <a href="mailto:%(addr)s?subject=%(subject)s">this link</a>'
)
REPLY_SEPARATOR_REGEX = re.compile(r'==== .* -=-==', re.MULTILINE|re.DOTALL)

ANSWER_SORT_METHODS = (#no translations needed here
    'latest', 'oldest', 'votes'
)
#todo: add assertion here that all sort methods are unique
#because they are keys to the hash used in implementations
#of Q.run_advanced_search

DEFAULT_POST_SORT_METHOD = 'activity-desc'
POST_SCOPE_LIST = (
    ('all', _('all')),
    ('unanswered', _('unanswered')),
    ('followed', _('followed')),
)
DEFAULT_POST_SCOPE = 'all'

TAG_LIST_FORMAT_CHOICES = (
    ('list', _('list')),
    ('cloud', _('cloud')),
)

PAGE_SIZE_CHOICES = (('10', '10',), ('30', '30',), ('50', '50',),)
ANSWERS_PAGE_SIZE = 10
QUESTIONS_PER_PAGE_USER_CHOICES = ((10, u'10'), (30, u'30'), (50, u'50'),)

UNANSWERED_QUESTION_MEANING_CHOICES = (
    ('NO_ANSWERS', _('Question has no answers')),
    ('NO_ACCEPTED_ANSWERS', _('Question has no accepted answers')),
)
#todo: implement this
#    ('NO_UPVOTED_ANSWERS',),
#)

#todo:
#this probably needs to be language-specific
#and selectable/changeable from the admin interface
#however it will be hard to expect that people will type
#correct regexes - plus this must be an anchored regex
#to do full string match
#IMPRTANT: tag related regexes must be portable between js and python
TAG_CHARS = r'\w+.#-'
TAG_REGEX_BARE = r'[%s]+' % TAG_CHARS
TAG_REGEX = r'^%s$' % TAG_REGEX_BARE
TAG_SPLIT_REGEX = r'[ ,]+'
TAG_SEP = ',' # has to be valid TAG_SPLIT_REGEX char and MUST NOT be in const.TAG_CHARS
#!!! see const.message_keys.TAG_WRONG_CHARS_MESSAGE
EMAIL_REGEX = re.compile(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b', re.I)

TYPE_ACTIVITY_ASK_QUESTION = 1
TYPE_ACTIVITY_ANSWER = 2
TYPE_ACTIVITY_COMMENT_QUESTION = 3
TYPE_ACTIVITY_COMMENT_ANSWER = 4
TYPE_ACTIVITY_UPDATE_QUESTION = 5
TYPE_ACTIVITY_UPDATE_ANSWER = 6
TYPE_ACTIVITY_PRIZE = 7
TYPE_ACTIVITY_MARK_ANSWER = 8
TYPE_ACTIVITY_VOTE_UP = 9
TYPE_ACTIVITY_VOTE_DOWN = 10
TYPE_ACTIVITY_CANCEL_VOTE = 11
TYPE_ACTIVITY_DELETE_QUESTION = 12
TYPE_ACTIVITY_DELETE_ANSWER = 13
TYPE_ACTIVITY_MARK_OFFENSIVE = 14
TYPE_ACTIVITY_UPDATE_TAGS = 15
TYPE_ACTIVITY_FAVORITE = 16
TYPE_ACTIVITY_USER_FULL_UPDATED = 17
TYPE_ACTIVITY_EMAIL_UPDATE_SENT = 18
TYPE_ACTIVITY_MENTION = 19
TYPE_ACTIVITY_UNANSWERED_REMINDER_SENT = 20
TYPE_ACTIVITY_ACCEPT_ANSWER_REMINDER_SENT = 21
TYPE_ACTIVITY_CREATE_TAG_WIKI = 22
TYPE_ACTIVITY_UPDATE_TAG_WIKI = 23
TYPE_ACTIVITY_MODERATED_NEW_POST = 24
TYPE_ACTIVITY_MODERATED_POST_EDIT = 25
TYPE_ACTIVITY_CREATE_REJECT_REASON = 26
TYPE_ACTIVITY_UPDATE_REJECT_REASON = 27
TYPE_ACTIVITY_VALIDATION_EMAIL_SENT = 28
TYPE_ACTIVITY_POST_SHARED = 29
TYPE_ACTIVITY_ASK_TO_JOIN_GROUP = 30
#TYPE_ACTIVITY_EDIT_QUESTION = 17
#TYPE_ACTIVITY_EDIT_ANSWER = 18

#todo: rename this to TYPE_ACTIVITY_CHOICES
TYPE_ACTIVITY = (
    (TYPE_ACTIVITY_ASK_QUESTION, _('asked a question')),
    (TYPE_ACTIVITY_ANSWER, _('answered a question')),
    (TYPE_ACTIVITY_COMMENT_QUESTION, _('commented question')),
    (TYPE_ACTIVITY_COMMENT_ANSWER, _('commented answer')),
    (TYPE_ACTIVITY_UPDATE_QUESTION, _('edited question')),
    (TYPE_ACTIVITY_UPDATE_ANSWER, _('edited answer')),
    (TYPE_ACTIVITY_PRIZE, _('received badge')),
    (TYPE_ACTIVITY_MARK_ANSWER, _('marked best answer')),
    (TYPE_ACTIVITY_VOTE_UP, _('upvoted')),
    (TYPE_ACTIVITY_VOTE_DOWN, _('downvoted')),
    (TYPE_ACTIVITY_CANCEL_VOTE, _('canceled vote')),
    (TYPE_ACTIVITY_DELETE_QUESTION, _('deleted question')),
    (TYPE_ACTIVITY_DELETE_ANSWER, _('deleted answer')),
    (TYPE_ACTIVITY_MARK_OFFENSIVE, _('marked offensive')),
    (TYPE_ACTIVITY_UPDATE_TAGS, _('updated tags')),
    (TYPE_ACTIVITY_FAVORITE, _('selected favorite')),
    (TYPE_ACTIVITY_USER_FULL_UPDATED, _('completed user profile')),
    (TYPE_ACTIVITY_EMAIL_UPDATE_SENT, _('email update sent to user')),
    (TYPE_ACTIVITY_POST_SHARED, _('a post was shared')),
    (
        TYPE_ACTIVITY_UNANSWERED_REMINDER_SENT,
        _('reminder about unanswered questions sent'),
    ),
    (
        TYPE_ACTIVITY_ACCEPT_ANSWER_REMINDER_SENT,
        _('reminder about accepting the best answer sent'),
    ),
    (TYPE_ACTIVITY_MENTION, _('mentioned in the post')),
    (
        TYPE_ACTIVITY_CREATE_TAG_WIKI,
        _('created tag description'),
    ),
    (
        TYPE_ACTIVITY_UPDATE_TAG_WIKI,
        _('updated tag description')
    ),
    (TYPE_ACTIVITY_MODERATED_NEW_POST, _('made a new post')),
    (
        TYPE_ACTIVITY_MODERATED_POST_EDIT,
        _('made an edit')
    ),
    (
        TYPE_ACTIVITY_CREATE_REJECT_REASON,
        _('created post reject reason'),
    ),
    (
        TYPE_ACTIVITY_UPDATE_REJECT_REASON,
        _('updated post reject reason')
    ),
    (
        TYPE_ACTIVITY_VALIDATION_EMAIL_SENT,
        'sent email address validation message'#don't translate, internal
    ),
)


#MENTION activity is added implicitly, unfortunately
RESPONSE_ACTIVITY_TYPES_FOR_INSTANT_NOTIFICATIONS = (
    TYPE_ACTIVITY_COMMENT_QUESTION,
    TYPE_ACTIVITY_COMMENT_ANSWER,
    TYPE_ACTIVITY_UPDATE_ANSWER,
    TYPE_ACTIVITY_UPDATE_QUESTION,
    TYPE_ACTIVITY_ANSWER,
    TYPE_ACTIVITY_ASK_QUESTION,
    TYPE_ACTIVITY_POST_SHARED
)


#the same as for instant notifications for now
#MENTION activity is added implicitly, unfortunately
RESPONSE_ACTIVITY_TYPES_FOR_DISPLAY = (
    TYPE_ACTIVITY_ANSWER,
    TYPE_ACTIVITY_ASK_QUESTION,
    TYPE_ACTIVITY_COMMENT_QUESTION,
    TYPE_ACTIVITY_COMMENT_ANSWER,
    TYPE_ACTIVITY_UPDATE_ANSWER,
    TYPE_ACTIVITY_UPDATE_QUESTION,
    TYPE_ACTIVITY_POST_SHARED,
#    TYPE_ACTIVITY_PRIZE,
#    TYPE_ACTIVITY_MARK_ANSWER,
#    TYPE_ACTIVITY_VOTE_UP,
#    TYPE_ACTIVITY_VOTE_DOWN,
#    TYPE_ACTIVITY_CANCEL_VOTE,
#    TYPE_ACTIVITY_DELETE_QUESTION,
#    TYPE_ACTIVITY_DELETE_ANSWER,
#    TYPE_ACTIVITY_MARK_OFFENSIVE,
#    TYPE_ACTIVITY_FAVORITE,
)

RESPONSE_ACTIVITY_TYPE_MAP_FOR_TEMPLATES = {
    TYPE_ACTIVITY_COMMENT_QUESTION: 'question_comment',
    TYPE_ACTIVITY_COMMENT_ANSWER: 'answer_comment',
    TYPE_ACTIVITY_UPDATE_ANSWER: 'answer_update',
    TYPE_ACTIVITY_UPDATE_QUESTION: 'question_update',
    TYPE_ACTIVITY_ANSWER: 'new_answer',
    TYPE_ACTIVITY_ASK_QUESTION: 'new_question',
    TYPE_ACTIVITY_POST_SHARED: 'post_shared'
}

assert(
    set(RESPONSE_ACTIVITY_TYPES_FOR_INSTANT_NOTIFICATIONS) \
    == set(RESPONSE_ACTIVITY_TYPE_MAP_FOR_TEMPLATES.keys())
)

TYPE_RESPONSE = {
    'QUESTION_ANSWERED' : _('answered question'),
    'QUESTION_COMMENTED': _('commented question'),
    'ANSWER_COMMENTED'  : _('commented answer'),
    'ANSWER_ACCEPTED'   : _('accepted answer'),
}

POST_STATUS = {
    'closed': _('[closed]'),
    'deleted': _('[deleted]'),
    'default_version': _('initial version'),
    'retagged': _('retagged'),
    'private': _('[private]')
}

#choices used in email and display filters
INCLUDE_ALL = 0
EXCLUDE_IGNORED = 1
INCLUDE_INTERESTING = 2
INCLUDE_SUBSCRIBED = 3
TAG_DISPLAY_FILTER_STRATEGY_MINIMAL_CHOICES = (
    (INCLUDE_ALL, _('show all tags')),
    (EXCLUDE_IGNORED, _('exclude ignored tags')),
    (INCLUDE_INTERESTING, _('only interesting tags'))
)
TAG_DISPLAY_FILTER_STRATEGY_CHOICES = \
    TAG_DISPLAY_FILTER_STRATEGY_MINIMAL_CHOICES + \
    ((INCLUDE_SUBSCRIBED, _('only subscribed tags')),)

TAG_EMAIL_FILTER_SIMPLE_STRATEGY_CHOICES = (
    (INCLUDE_ALL, _('email for all tags')),
    (EXCLUDE_IGNORED, _('exclude ignored tags')),
    (INCLUDE_INTERESTING, _('only interesting tags')),
)

TAG_EMAIL_FILTER_ADVANCED_STRATEGY_CHOICES = (
    (INCLUDE_ALL, _('email for all tags')),
    (EXCLUDE_IGNORED, _('exclude ignored tags')),
    (INCLUDE_SUBSCRIBED, _('only subscribed tags')),
)

TAG_EMAIL_FILTER_FULL_STRATEGY_CHOICES = (
    (INCLUDE_ALL, _('email for all tags')),
    (EXCLUDE_IGNORED, _('exclude ignored tags')),
    (INCLUDE_INTERESTING, _('only interesting tags')),
    (INCLUDE_SUBSCRIBED, _('only subscribed tags')),
)

NOTIFICATION_DELIVERY_SCHEDULE_CHOICES = (
                            ('i',_('instantly')),
                            ('d',_('daily')),
                            ('w',_('weekly')),
                            ('n',_('no email')),
                        )

USERS_PAGE_SIZE = 28#todo: move it to settings?
USERNAME_REGEX_STRING = r'^[\w \-.@+\']+$'

GRAVATAR_TYPE_CHOICES = (
                            ('identicon',_('identicon')),
                            ('mm',_('mystery-man')),
                            ('monsterid',_('monsterid')),
                            ('wavatar',_('wavatar')),
                            ('retro',_('retro')),
                        )

#chars that can go before or after @mention
TWITTER_STYLE_MENTION_TERMINATION_CHARS = '\n ;:,.!?<>"\''

COMMENT_HARD_MAX_LENGTH = 2048

#user status ch
USER_STATUS_CHOICES = (
        #in addition to these there is administrator
        #admin status is determined by the User.is_superuser() call
        ('m', _('moderator')), #user with moderation privilege
        ('a', _('approved')), #regular user
        ('w', _('watched')), #regular user placed on the moderation watch
        ('s', _('suspended')), #suspended user who cannot post new stuff
        ('b', _('blocked')), #blocked
)
DEFAULT_USER_STATUS = 'w'

#number of items to show in user views
USER_VIEW_DATA_SIZE = 50

#not really dependency, but external links, which it would
#be nice to test for correctness from time to time
DEPENDENCY_URLS = {
    'akismet': 'https://akismet.com/signup/',
    'cc-by-sa': 'http://creativecommons.org/licenses/by-sa/3.0/legalcode',
    'embedding-video': \
        'http://askbot.org/doc/optional-modules.html#embedding-video',
    'favicon': 'http://en.wikipedia.org/wiki/Favicon',
    'facebook-apps': 'http://www.facebook.com/developers/createapp.php',
    'google-webmaster-tools': 'https://www.google.com/webmasters/tools/home',
    'identica-apps': 'http://identi.ca/settings/oauthapps',
    'noscript': 'https://www.google.com/support/bin/answer.py?answer=23852',
    'linkedin-apps': 'https://www.linkedin.com/secure/developer',
    'mathjax': 'http://www.mathjax.org/resources/docs/?installation.html',
    'recaptcha': 'http://google.com/recaptcha',
    'twitter-apps': 'http://dev.twitter.com/apps/',
}

PASSWORD_MIN_LENGTH = 8

GOLD_BADGE = 1
SILVER_BADGE = 2
BRONZE_BADGE = 3
BADGE_TYPE_CHOICES = (
    (GOLD_BADGE,   _('gold')),
    (SILVER_BADGE, _('silver')),
    (BRONZE_BADGE, _('bronze')),
)
BADGE_CSS_CLASSES = {
    GOLD_BADGE: 'badge1',
    SILVER_BADGE: 'badge2',
    BRONZE_BADGE: 'badge3',
}
BADGE_DISPLAY_SYMBOL = '&#9679;'

MIN_REPUTATION = 1

AVATAR_STATUS_CHOICE = (
    ('n', _('None')),
    ('g', _('Gravatar')),#only if user has real uploaded gravatar
    ('a', _('Uploaded Avatar')),#avatar uploaded locally - with django-avatar app
)

SEARCH_ORDER_BY = (
                    ('-added_at', _('date descendant')),
                    ('added_at', _('date ascendant')),
                    ('-last_activity_at', _('activity descendant')),
                    ('last_activity_at', _('activity ascendant')),
                    ('-answer_count', _('answers descendant')),
                    ('answer_count', _('answers ascendant')),
                    ('-points', _('votes descendant')),
                    ('points', _('votes ascendant')),
                  )

DEFAULT_QUESTION_WIDGET_STYLE = """
@import url('http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700');
body {
    overflow: hidden;
}

#container {
    width: 200px;
    height: 350px;
}
ul {
    list-style: none;
    padding: 5px;
    margin: 5px;
}
li {
    border-bottom: #CCC 1px solid;
    padding-bottom: 5px;
    padding-top: 5px;
}
li:last-child {
    border: none;
}
a {
    text-decoration: none;
    color: #464646;
    font-family: 'Yanone Kaffeesatz', sans-serif;
    font-size: 15px;
}
"""

#an exception import * because that file has only strings
from askbot.const.message_keys import *
