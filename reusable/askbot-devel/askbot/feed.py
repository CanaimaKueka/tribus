"""
#-------------------------------------------------------------------------------
# Name:        Syndication feed class for subscription
# Purpose:
#
# Author:      Mike
#
# Created:     29/01/2009
# Copyright:   (c) CNPROG.COM 2009
# Licence:     GPL V2
#-------------------------------------------------------------------------------
"""
#!/usr/bin/env python
#encoding:utf-8
from django.contrib.syndication.views import Feed

import itertools

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from askbot.conf import settings as askbot_settings
from askbot.models import Post
from askbot.utils.html import site_url

class RssIndividualQuestionFeed(Feed):
    """rss feed class for particular questions
    """

    def title(self):
        return askbot_settings.APP_TITLE + _(' - ') + \
                _('Individual question feed')

    def feed_copyright(self):
        return askbot_settings.APP_COPYRIGHT

    def description(self):
        return askbot_settings.APP_DESCRIPTION

    def get_object(self, request, pk):
        if askbot_settings.RSS_ENABLED is False:
            raise Http404
        #hack to get the request object into the Feed class
        self.request = request
        return Post.objects.get_questions().get(id__exact = pk)

    def item_link(self, item):
        """get full url to the item
        """
        return site_url(item.get_absolute_url())

    def link(self):
        return site_url(reverse('questions'))

    def item_pubdate(self, item):
        """get date of creation for the item
        """
        return item.added_at

    def items(self, item):
        """get content items for the feed
        ordered as: question, question comments,
        then for each answer - the answer itself, then
        answer comments
        """
        chain_elements = list()
        chain_elements.append([item,])
        chain_elements.append(
            Post.objects.get_comments().filter(parent=item)
        )

        answers = Post.objects.get_answers().filter(thread = item.thread)

        for answer in answers:
            chain_elements.append([answer,])
            chain_elements.append(
                Post.objects.get_comments().filter(parent=answer)
            )

        return itertools.chain(*chain_elements)

    def item_title(self, item):
        """returns the title for the item
        """
        title = item
        if item.post_type == "question":
            self.title = item
        elif item.post_type == "answer":
            title = "Answer by %s for %s " % (item.author, self.title)
        elif item.post_type == "comment":
            title = "Comment by %s for %s" % (item.author, self.title)
        return title

    def item_description(self, item):
        """returns the description for the item
        """
        return item.text


class RssLastestQuestionsFeed(Feed):
    """rss feed class for the latest questions
    """

    def title(self):
        return askbot_settings.APP_TITLE + _(' - ') + \
                _('Individual question feed')

    def feed_copyright(self):
        return askbot_settings.APP_COPYRIGHT

    def description(self):
        return askbot_settings.APP_DESCRIPTION

    def item_link(self, item):
        """get full url to the item
        """
        return site_url(item.get_absolute_url())

    def link(self):
        return site_url(reverse('questions'))

    def item_author_name(self, item):
        """get name of author
        """
        return item.author.username

    def item_author_link(self, item):
        """get url of the author's profile
        """
        return site_url(item.author.get_profile_url())

    def item_pubdate(self, item):
        """get date of creation for the item
        """
        return item.added_at

    def item_guid(self, item):
        """returns url without the slug
        because the slug can change
        """
        return self.link() + item.get_absolute_url(no_slug = True)

    def item_description(self, item):
        """returns the description for the item
        """
        return item.text

    def items(self, item):
        """get questions for the feed
        """
        if askbot_settings.RSS_ENABLED is False:
            raise Http404
        #initial filtering
        qs = Post.objects.get_questions().filter(deleted=False)

        #get search string and tags from GET
        query = self.request.GET.get("q", None)
        tags = self.request.GET.getlist("tags")

        if query:
            #if there's a search string, use the
            #question search method
            qs = qs.get_by_text_query(query)

        if tags:
            #if there are tags in GET, filter the
            #questions additionally
            for tag in tags:
                qs = qs.filter(thread__tags__name = tag)

        return qs.order_by('-thread__last_activity_at')[:30]

    #hack to get the request object into the Feed class
    def get_feed(self, obj, request):
        self.request = request
        return super(RssLastestQuestionsFeed, self).get_feed(obj, request)

def main():
    """main function for use as a script
    """
    pass

if __name__ == '__main__':
    main()
