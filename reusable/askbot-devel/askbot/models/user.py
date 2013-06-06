import datetime
import logging
import re
from django.db import models
from django.db.backends.dummy.base import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.contrib.auth.models import Group as AuthGroup
from django.core import exceptions
from django.forms import EmailField, URLField
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.utils.html import strip_tags
from askbot import const
from askbot.conf import settings as askbot_settings
from askbot.utils import functions
from askbot.models.base import BaseQuerySetManager
from askbot.models.tag import Tag
from askbot.models.tag import clean_group_name#todo - delete this
from askbot.models.tag import get_tags_by_names
from askbot.forms import DomainNameField
from askbot.utils.forms import email_is_allowed

PERSONAL_GROUP_NAME_PREFIX = '_personal_'

class ResponseAndMentionActivityManager(models.Manager):
    def get_query_set(self):
        response_types = const.RESPONSE_ACTIVITY_TYPES_FOR_DISPLAY
        response_types += (const.TYPE_ACTIVITY_MENTION, )
        return super(
                    ResponseAndMentionActivityManager,
                    self
                ).get_query_set().filter(
                    activity_type__in = response_types
                )

class ActivityManager(models.Manager):
    def get_all_origin_posts(self):
        #todo: redo this with query sets
        origin_posts = set()
        for m in self.all():
            post = m.content_object
            if post and hasattr(post, 'get_origin_post'):
                origin_posts.add(post.get_origin_post())
            else:
                logging.debug(
                            'method get_origin_post() not implemented for %s' \
                            % unicode(post)
                        )
        return list(origin_posts)

    def create_new_mention(
                self,
                mentioned_by = None,
                mentioned_whom = None,
                mentioned_at = None,
                mentioned_in = None,
                reported = None
            ):

        #todo: automate this using python inspect module
        kwargs = dict()

        kwargs['activity_type'] = const.TYPE_ACTIVITY_MENTION

        if mentioned_at:
            #todo: handle cases with rich lookups here like __lt
            kwargs['active_at'] = mentioned_at

        if mentioned_by:
            kwargs['user'] = mentioned_by

        if mentioned_in:
            if functions.is_iterable(mentioned_in):
                raise NotImplementedError('mentioned_in only works for single items')
            else:
                post_content_type = ContentType.objects.get_for_model(mentioned_in)
                kwargs['content_type'] = post_content_type
                kwargs['object_id'] = mentioned_in.id

        if reported == True:
            kwargs['is_auditted'] = True
        else:
            kwargs['is_auditted'] = False

        mention_activity = Activity(**kwargs)
        mention_activity.question = mentioned_in.get_origin_post()
        mention_activity.save()

        if mentioned_whom:
            assert(isinstance(mentioned_whom, User))
            mention_activity.add_recipients([mentioned_whom])
            mentioned_whom.update_response_counts()

        return mention_activity

    def get_mentions(
                self,
                mentioned_by = None,
                mentioned_whom = None,
                mentioned_at = None,
                mentioned_in = None,
                reported = None,
                mentioned_at__lt = None,
            ):
        """extract mention-type activity objects
        todo: implement better rich field lookups
        """

        kwargs = dict()

        kwargs['activity_type'] = const.TYPE_ACTIVITY_MENTION

        if mentioned_at:
            #todo: handle cases with rich lookups here like __lt, __gt and others
            kwargs['active_at'] = mentioned_at
        elif mentioned_at__lt:
            kwargs['active_at__lt'] = mentioned_at__lt

        if mentioned_by:
            kwargs['user'] = mentioned_by

        if mentioned_whom:
            if functions.is_iterable(mentioned_whom):
                kwargs['recipients__in'] = mentioned_whom
            else:
                kwargs['recipients__in'] = (mentioned_whom,)

        if mentioned_in:
            if functions.is_iterable(mentioned_in):
                it = iter(mentioned_in)
                raise NotImplementedError('mentioned_in only works for single items')
            else:
                post_content_type = ContentType.objects.get_for_model(mentioned_in)
                kwargs['content_type'] = post_content_type
                kwargs['object_id'] = mentioned_in.id

        if reported == True:
            kwargs['is_auditted'] = True
        else:
            kwargs['is_auditted'] = False

        return self.filter(**kwargs)


class ActivityAuditStatus(models.Model):
    """bridge "through" relation between activity and users"""
    STATUS_NEW = 0
    STATUS_SEEN = 1
    STATUS_CHOICES = (
        (STATUS_NEW, 'new'),
        (STATUS_SEEN, 'seen')
    )
    user = models.ForeignKey(User)
    activity = models.ForeignKey('Activity')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)

    class Meta:
        unique_together = ('user', 'activity')
        app_label = 'askbot'
        db_table = 'askbot_activityauditstatus'

    def is_new(self):
        return (self.status == self.STATUS_NEW)


class Activity(models.Model):
    """
    We keep some history data for user activities
    """
    user = models.ForeignKey(User)
    receiving_users = models.ManyToManyField(User, related_name='received_activity')
    recipients = models.ManyToManyField(User, through=ActivityAuditStatus, related_name='incoming_activity')
    activity_type = models.SmallIntegerField(choices = const.TYPE_ACTIVITY)
    active_at = models.DateTimeField(default=datetime.datetime.now)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    #todo: remove this denorm question field when Post model is set up
    question = models.ForeignKey('Post', null=True)

    is_auditted = models.BooleanField(default=False)
    #add summary field.
    summary = models.TextField(default='')

    objects = ActivityManager()
    responses_and_mentions = ResponseAndMentionActivityManager()

    def __unicode__(self):
        return u'[%s] was active at %s' % (self.user.username, self.active_at)

    class Meta:
        app_label = 'askbot'
        db_table = u'activity'

    def add_recipients(self, recipients):
        """have to use a special method, because django does not allow
        auto-adding to M2M with "through" model
        """
        for recipient in recipients:
            #todo: may optimize for bulk addition
            aas = ActivityAuditStatus(user = recipient, activity = self)
            aas.save()

    def get_mentioned_user(self):
        assert(self.activity_type == const.TYPE_ACTIVITY_MENTION)
        user_qs = self.recipients.all()
        user_count = len(user_qs)
        if user_count == 0:
            return None
        assert(user_count == 1)
        return user_qs[0]

    def get_snippet(self, max_length = 120):
        return self.content_object.get_snippet(max_length)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

class EmailFeedSettingManager(models.Manager):
    def filter_subscribers(
                        self,
                        potential_subscribers = None,
                        feed_type = None,
                        frequency = None
                    ):
        """returns set of users who have matching subscriptions
        and if potential_subscribers is not none, search will
        be limited to only potential subscribers,

        otherwise search is unrestricted

        todo: when EmailFeedSetting is merged into user table
        this method may become unnecessary
        """
        matching_feeds = self.filter(
                                        feed_type = feed_type,
                                        frequency = frequency
                                    )
        if potential_subscribers is not None:
            matching_feeds = matching_feeds.filter(
                            subscriber__in = potential_subscribers
                        )
        subscriber_set = set()
        for feed in matching_feeds:
            subscriber_set.add(feed.subscriber)

        return subscriber_set

class EmailFeedSetting(models.Model):
    #definitions of delays before notification for each type of notification frequency
    DELTA_TABLE = {
        'i':datetime.timedelta(-1),#instant emails are processed separately
        'd':datetime.timedelta(1),
        'w':datetime.timedelta(7),
        'n':datetime.timedelta(-1),
    }
    #definitions of feed schedule types
    FEED_TYPES = (
            'q_ask', #questions that user asks
            'q_all', #enture forum, tag filtered
            'q_ans', #questions that user answers
            'q_sel', #questions that user decides to follow
            'm_and_c' #comments and mentions of user anywhere
    )
    #email delivery schedule when no email is sent at all
    NO_EMAIL_SCHEDULE = {
        'q_ask': 'n',
        'q_ans': 'n',
        'q_all': 'n',
        'q_sel': 'n',
        'm_and_c': 'n'
    }
    MAX_EMAIL_SCHEDULE = {
        'q_ask': 'i',
        'q_ans': 'i',
        'q_all': 'i',
        'q_sel': 'i',
        'm_and_c': 'i'
    }
    FEED_TYPE_CHOICES = (
                    ('q_all', ugettext_lazy('Entire forum')),
                    ('q_ask', ugettext_lazy('Questions that I asked')),
                    ('q_ans', ugettext_lazy('Questions that I answered')),
                    ('q_sel', ugettext_lazy('Individually selected questions')),
                    ('m_and_c', ugettext_lazy('Mentions and comment responses')),
                    )
    UPDATE_FREQUENCY = (
                    ('i', ugettext_lazy('Instantly')),
                    ('d', ugettext_lazy('Daily')),
                    ('w', ugettext_lazy('Weekly')),
                    ('n', ugettext_lazy('No email')),
                   )


    subscriber = models.ForeignKey(User, related_name='notification_subscriptions')
    feed_type = models.CharField(max_length=16, choices=FEED_TYPE_CHOICES)
    frequency = models.CharField(
                                    max_length=8,
                                    choices=const.NOTIFICATION_DELIVERY_SCHEDULE_CHOICES,
                                    default='n',
                                )
    added_at = models.DateTimeField(auto_now_add=True)
    reported_at = models.DateTimeField(null=True)
    objects = EmailFeedSettingManager()

    class Meta:
        #added to make account merges work properly
        unique_together = ('subscriber', 'feed_type')
        app_label = 'askbot'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        if self.reported_at is None:
            reported_at = "'not yet'"
        else:
            reported_at = '%s' % self.reported_at.strftime('%d/%m/%y %H:%M')
        return u'Email feed for %s type=%s, frequency=%s, reported_at=%s' % (
                                                     self.subscriber,
                                                     self.feed_type,
                                                     self.frequency,
                                                     reported_at
                                                 )

    def save(self,*args,**kwargs):
        type = self.feed_type
        subscriber = self.subscriber
        similar = self.__class__.objects.filter(
                                            feed_type=type,
                                            subscriber=subscriber
                                        ).exclude(pk=self.id)
        if len(similar) > 0:
            raise IntegrityError('email feed setting already exists')
        super(EmailFeedSetting,self).save(*args,**kwargs)

    def get_previous_report_cutoff_time(self):
        now = datetime.datetime.now()
        return now - self.DELTA_TABLE[self.frequency]

    def should_send_now(self):
        now = datetime.datetime.now()
        cutoff_time = self.get_previous_report_cutoff_time()
        if self.reported_at == None or self.reported_at <= cutoff_time:
            return True
        else:
            return False

    def mark_reported_now(self):
        self.reported_at = datetime.datetime.now()
        self.save()


class AuthUserGroups(models.Model):
    """explicit model for the auth_user_groups bridge table.
    """
    group = models.ForeignKey(AuthGroup)
    user = models.ForeignKey(User)

    class Meta:
        app_label = 'auth'
        unique_together = ('group', 'user')
        db_table = 'auth_user_groups'
        managed = False


class GroupMembership(AuthUserGroups):
    """contains one-to-one relation to ``auth_user_group``
    and extra membership profile fields"""
    #note: this may hold info on when user joined, etc
    NONE = -1#not part of the choices as for this records should be just missing
    PENDING = 0
    FULL = 1
    LEVEL_CHOICES = (#'none' is by absence of membership
        (PENDING, 'pending'),
        (FULL, 'full')
    )
    ALL_LEVEL_CHOICES = LEVEL_CHOICES + ((NONE, 'none'),)

    level = models.SmallIntegerField(
                        default=FULL,
                        choices=LEVEL_CHOICES,
                    )


    class Meta:
        app_label = 'askbot'

    @classmethod
    def get_level_value_display(cls, level):
        """returns verbose value given a numerical value
        includes the "fanthom" NONE
        """
        values_dict = dict(cls.ALL_LEVEL_CHOICES)
        return values_dict[level]


class GroupQuerySet(models.query.QuerySet):
    """Custom query set for the group"""

    def exclude_personal(self):
        """excludes the personal groups"""
        return self.exclude(
            name__startswith=PERSONAL_GROUP_NAME_PREFIX
        )

    def get_personal(self):
        """filters for the personal groups"""
        return self.filter(
            name__startswith=PERSONAL_GROUP_NAME_PREFIX
        )

    def get_for_user(self, user=None, private=False):
        if private:
            global_group = Group.objects.get_global_group()
            return self.filter(
                        user=user
                    ).exclude(id=global_group.id)
        else:
            return self.filter(user = user)

    def get_by_name(self, group_name = None):
        return self.get(name = clean_group_name(group_name))


class GroupManager(BaseQuerySetManager):
    """model manager for askbot groups"""

    def get_query_set(self):
        return GroupQuerySet(self.model)

    def get_global_group(self):
        """Returns the global group,
        if necessary, creates one
        """
        #todo: when groups are disconnected from tags,
        #find comment as shown below in the test cases and
        #revert the values
        #todo: change groups to django groups
        group_name = askbot_settings.GLOBAL_GROUP_NAME
        try:
            return self.get_query_set().get(name=group_name)
        except Group.DoesNotExist:
            return self.get_query_set().create(name=group_name)

    def create(self, **kwargs):
        name = kwargs['name']
        try:
            group_ptr = AuthGroup.objects.get(name=name)
            kwargs['group_ptr'] = group_ptr
        except AuthGroup.DoesNotExist:
            pass
        return super(GroupManager, self).create(**kwargs)

    def get_or_create(self, name = None, user = None, openness=None):
        """creates a group tag or finds one, if exists"""
        #todo: here we might fill out the group profile
        try:
            #iexact is important!!! b/c we don't want case variants
            #of tags
            group = self.get(name__iexact = name)
        except self.model.DoesNotExist:
            if openness is None:
                group = self.create(name=name)
            else:
                group = self.create(name=name, openness=openness)
        return group


class Group(AuthGroup):
    """group profile for askbot"""
    OPEN = 0
    MODERATED = 1
    CLOSED = 2
    OPENNESS_CHOICES = (
        (OPEN, 'open'),
        (MODERATED, 'moderated'),
        (CLOSED, 'closed'),
    )
    logo_url = models.URLField(null=True)
    description = models.OneToOneField(
                    'Post', related_name='described_group',
                    null=True, blank=True
                )
    moderate_email = models.BooleanField(default=True)
    moderate_answers_to_enquirers = models.BooleanField(
                        default=False,
                        help_text='If true, answers to outsiders questions '
                                'will be shown to the enquirers only when '
                                'selected by the group moderators.'
                    )
    openness = models.SmallIntegerField(default=CLOSED, choices=OPENNESS_CHOICES)
    #preapproved email addresses and domain names to auto-join groups
    #trick - the field is padded with space and all tokens are space separated
    preapproved_emails = models.TextField(
                            null = True, blank = True, default = ''
                        )
    #only domains - without the '@' or anything before them
    preapproved_email_domains = models.TextField(
                            null = True, blank = True, default = ''
                        )

    is_vip = models.BooleanField(default=False)

    objects = GroupManager()

    class Meta:
        app_label = 'askbot'
        db_table = 'askbot_group'

    def get_moderators(self):
        """returns group moderators"""
        user_filter = models.Q(is_superuser=True) | models.Q(status='m')
        user_filter = user_filter & models.Q(groups__in=[self])
        return User.objects.filter(user_filter)

    def has_moderator(self, user):
        """true, if user is a group moderator"""
        mod_ids = self.get_moderators().values_list('id', flat=True)
        return user.id in mod_ids

    def get_openness_choices(self):
        """gives answers to question
        "How can users join this group?"
        """
        return (
            (Group.OPEN, _('Can join when they want')),
            (Group.MODERATED, _('Users ask permission')),
            (Group.CLOSED, _('Moderator adds users'))
        )

    def get_openness_level_for_user(self, user):
        """returns descriptive value, because it is to be used in the
        templates. The value must match the verbose versions of the
        openness choices!!!
        """
        if user.is_anonymous():
            return 'closed'

        #a special case - automatic global group cannot be joined or left
        if self.name == askbot_settings.GLOBAL_GROUP_NAME:
            return 'closed'

        #todo - return 'closed' for internal per user groups too

        if self.openness == Group.OPEN:
            return 'open'

        if user.is_administrator_or_moderator():
            return 'open'

        #relying on a specific method of storage
        if email_is_allowed(
            user.email,
            allowed_emails=self.preapproved_emails,
            allowed_email_domains=self.preapproved_email_domains
        ):
            return 'open'

        if self.openness == Group.MODERATED:
            return 'moderated'

        return 'closed'

    def is_personal(self):
        """``True`` if the group is personal"""
        return self.name.startswith(PERSONAL_GROUP_NAME_PREFIX)

    def clean(self):
        """called in `save()`
        """
        emails = functions.split_list(self.preapproved_emails)
        email_field = EmailField()
        try:
            map(lambda v: email_field.clean(v), emails)
        except exceptions.ValidationError:
            raise exceptions.ValidationError(
                _('Please give a list of valid email addresses.')
            )
        self.preapproved_emails = ' ' + '\n'.join(emails) + ' '

        domains = functions.split_list(self.preapproved_email_domains)
        domain_field = DomainNameField()
        try:
            map(lambda v: domain_field.clean(v), domains)
        except exceptions.ValidationError:
            raise exceptions.ValidationError(
                _('Please give a list of valid email domain names.')
            )
        self.preapproved_email_domains = ' ' + '\n'.join(domains) + ' '

    def save(self, *args, **kwargs):
        self.clean()
        super(Group, self).save(*args, **kwargs)

class BulkTagSubscriptionManager(BaseQuerySetManager):

    def create(
                self, tag_names=None,
                user_list=None, group_list=None,
                tag_author=None,  **kwargs
            ):

        tag_names = tag_names or []
        user_list = user_list or []
        group_list = group_list or []

        new_object = super(BulkTagSubscriptionManager, self).create(**kwargs)
        tag_name_list = []

        if tag_names:
            tags, new_tag_names = get_tags_by_names(tag_names)
            if new_tag_names:
                assert(tag_author)

            tags_id_list= [tag.id for tag in tags]
            tag_name_list = [tag.name for tag in tags]

            new_tags = Tag.objects.create_in_bulk(
                                        tag_names=new_tag_names,
                                        user=tag_author
                                    )

            tags_id_list.extend([tag.id for tag in new_tags])
            tag_name_list.extend([tag.name for tag in new_tags])

            new_object.tags.add(*tags_id_list)

        if user_list:
            user_ids = []
            for user in user_list:
                user_ids.append(user.id)
                user.mark_tags(tagnames=tag_name_list,
                               reason='subscribed',
                               action='add')

            new_object.users.add(*user_ids)

        if group_list:
            group_ids = []
            for group in group_list:
                #TODO: do the group marked tag thing here
                group_ids.append(group.id)
            new_object.groups.add(*group_ids)

        return new_object


class BulkTagSubscription(models.Model):
    date_added = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    users = models.ManyToManyField(User)
    groups = models.ManyToManyField(Group)

    objects = BulkTagSubscriptionManager()

    def tag_list(self):
        return [tag.name for tag in self.tags.all()]

    class Meta:
        app_label = 'askbot'
        ordering = ['-date_added']
