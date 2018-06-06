# Peter Quill Twitter bot @starlord_p
# Twitter: https://twitter.com/starlord_p/

from nltk.chat.util import Chat, reflections
from nltk.corpus import stopwords
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import pairs
import search


def remove_stop_words(text):
    stop_words = stopwords.words("english")
    return ' '.join([word for word in text.split() if word not in stop_words])


def reply(auth, tweet):
    api = tweepy.API(auth)
    try:
        tweetId = tweet.id
        username = tweet.user.screen_name
        text = tweet.text
        text = text.replace('@starlord_p ', '')
        if "would like to know" in text:
            text = text.replace('I would like to know', '')
            text = remove_stop_words(text)
            print(text)
            result = search.search_guides(text)
            api.update_status("@" + username + " Maybe this guide would help: " + result, in_reply_to_status_id=tweetId)
        else:
            phrase = Chat(pairs.eliza(), reflections).respond(text)
            api.update_status("@" + username + " " + phrase, in_reply_to_status_id=tweetId)
            print("Tweet : " + text)
            print("Replied with : " + phrase)
    except tweepy.TweepError as e:
        print(e.reason)


class Listener(StreamListener):

    def on_status(self, data):
        print(data)
        reply(auth, data)
        return (True)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    auth = OAuthHandler(os.environ['C_KEY'], os.environ['C_SECRET'])
    auth.set_access_token(os.environ['A_TOKEN'], os.environ['A_TOKEN_SECRET'])

    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=["@starlord_p"])

