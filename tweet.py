from nltk.chat.util import Chat, reflections
from nltk.corpus import stopwords
import tweepy
import pairs
import search
import summarize


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
        if 'like to know' in text:
            text = text.replace('I would like to know', '')
            text = remove_stop_words(text)
            print(text)
            result = search.search_guides(text)
            if result:
                api.update_status("@" + username + " Maybe this guide would help: " + result, in_reply_to_status_id=tweetId)
            else:
                api.update_status("@" + username + "I'm not sure how to help with that", in_reply_to_status_id=tweetId)
        elif 'tweet something about' in text:
            tweet = summarize.compile_tweet(text)
            print(tweet)
            api.update_status(status=tweet)
        else:
            phrase = Chat(pairs.eliza(), reflections).respond(text)
            api.update_status("@" + username + " " + phrase, in_reply_to_status_id=tweetId)
            print("Tweet : " + text)
            print("Replied with : " + phrase)
    except tweepy.TweepError as e:
        print(e.reason)


def send_tweet(auth, tweet):
    api = tweepy.API(auth)
    try:
        api.update_status(status=tweet)
        print(tweet)
    except tweepy.TweepError as e:
        print(e.reason)

