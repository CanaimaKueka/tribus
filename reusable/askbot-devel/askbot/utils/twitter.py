import urllib
from askbot.deps.django_authopenid.util import OAuthConnection

class Twitter(OAuthConnection):
    def __init__(self):
        super(Twitter, self).__init__('twitter')
        self.tweet_url = 'https://api.twitter.com/1.1/statuses/update.json'

    def tweet(self, text, access_token=None):
        client = self.get_client(access_token)
        body = urllib.urlencode({'status': text})
        return self.send_request(client, self.tweet_url, 'POST', body=body)
