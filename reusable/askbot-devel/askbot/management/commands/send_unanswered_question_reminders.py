from django.core.management.base import NoArgsCommand
from django.template.loader import get_template
from askbot import models
from askbot import const
from askbot.conf import settings as askbot_settings
from django.utils.translation import ungettext
from askbot import mail
from askbot.utils.classes import ReminderSchedule
from askbot.models.question import Thread
from askbot.utils.html import site_url
from django.template import Context

DEBUG_THIS_COMMAND = False

class Command(NoArgsCommand):
    """management command that sends reminders
    about unanswered questions to all users
    """
    def handle_noargs(self, **options):
        if askbot_settings.ENABLE_EMAIL_ALERTS == False:
            return
        if askbot_settings.ENABLE_UNANSWERED_REMINDERS == False:
            return
        #get questions without answers, excluding closed and deleted
        #order it by descending added_at date
        schedule = ReminderSchedule(
            askbot_settings.DAYS_BEFORE_SENDING_UNANSWERED_REMINDER,
            askbot_settings.UNANSWERED_REMINDER_FREQUENCY,
            max_reminders = askbot_settings.MAX_UNANSWERED_REMINDERS
        )

        questions = models.Post.objects.get_questions().exclude(
                                        thread__closed = True
                                    ).exclude(
                                        deleted = True
                                    ).added_between(
                                        start = schedule.start_cutoff_date,
                                        end = schedule.end_cutoff_date
                                    ).filter(
                                        thread__answer_count = 0
                                    ).order_by('-added_at')
        #for all users, excluding blocked
        #for each user, select a tag filtered subset
        #format the email reminder and send it
        for user in models.User.objects.exclude(status = 'b'):
            user_questions = questions.exclude(author = user)
            user_questions = user.get_tag_filtered_questions(user_questions)

            if askbot_settings.GROUPS_ENABLED:
                user_groups = user.get_groups()
                user_questions = user_questions.filter(groups__in = user_groups)

            final_question_list = user_questions.get_questions_needing_reminder(
                user = user,
                activity_type = const.TYPE_ACTIVITY_UNANSWERED_REMINDER_SENT,
                recurrence_delay = schedule.recurrence_delay
            )

            question_count = len(final_question_list)
            if question_count == 0:
                continue

            threads = Thread.objects.filter(id__in=[qq.thread_id for qq in final_question_list])
            tag_summary = Thread.objects.get_tag_summary_from_threads(threads)

            subject_line = ungettext(
                '%(question_count)d unanswered question about %(topics)s',
                '%(question_count)d unanswered questions about %(topics)s',
                question_count
            ) % {
                'question_count': question_count,
                'topics': tag_summary
            }

            data = {
                    'site_url': site_url(''),
                    'questions': final_question_list,
                    'subject_line': subject_line
                   }

            template = get_template('email/unanswered_question_reminder.html')
            body_text = template.render(Context(data))#todo: set lang


            if DEBUG_THIS_COMMAND:
                print "User: %s<br>\nSubject:%s<br>\nText: %s<br>\n" % \
                    (user.email, subject_line, body_text)
            else:
                mail.send_mail(
                    subject_line = subject_line,
                    body_text = body_text,
                    recipient_list = (user.email,)
                )
