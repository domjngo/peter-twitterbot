# Peter Quill Twitter bot @starlord_p
# Twitter: https://twitter.com/starlord_p/

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import tweet


class Listener(StreamListener):

    def on_status(self, data):
        print(data)
        if '@starlord_p' in data:
            tweet.reply(auth, data)
        return (True)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    auth = OAuthHandler(os.environ['C_KEY'], os.environ['C_SECRET'])
    auth.set_access_token(os.environ['A_TOKEN'], os.environ['A_TOKEN_SECRET'])

    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=["@starlord_p"])

