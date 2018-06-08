import re
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from collections import defaultdict
from heapq import nlargest
import link

nltk.data.path.append('./nltk_data/')


def compile_tweet(text):
    url = get_url(text)
    summary = summarize_article(url).strip('.')
    tags = get_tags(url)
    tiny_url = link.make_tiny(url)
    return summary + tags + ' ' + tiny_url


def get_url(text):
    url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
    if url:
        return url
    return False


def get_article(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    try:
        article = soup.find('article').get_text()
        article = re.sub('\n\n', '. ', article)
        article = re.sub('\s+', ' ', article).strip()
    except AttributeError:
        article = soup.find('article')
    if article:
        return article
    return False


def get_tags(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    tags = soup.find('meta', {'property' : 'article:tag'})
    tags = re.sub(' ', '', tags['content'])
    tags = re.sub('&', '', tags)
    tag_list = tags.split(',')
    tag_list = [ x for x in tag_list if 'news' not in x ]
    tag_list = [ x for x in tag_list if len(x) < 20 ]
    x = len(tag_list)
    if tag_list:
        hash_tags = ''
        for i in range(x):
            hash_tags = hash_tags + ' #' + tag_list[i]
            if i == 2:
                break
        return hash_tags
    return ''


def summarize_article(url):
    article = get_article(url)
    sentences = sent_tokenize(article)
    sentences = list(set(sentences))
    sentences = [x for x in sentences if len(x) < 188]
    words = word_tokenize(article.lower())
    _stopwords = set(stopwords.words('english') + list(punctuation) + my_stopwords())
    useful_words = [word for word in words if word not in _stopwords]
    useful_words = clean_list(useful_words)
    freq = FreqDist(useful_words)
    ranking = defaultdict(int)
    for i, sent in enumerate(sentences):
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]
    sents_idx = nlargest(1, ranking, key=ranking.get)
    summary = [sentences[j] for j in sorted(sents_idx)]
    return summary[0]


def clean_list(word_list):
    while '–' in word_list:
        word_list.remove('–')
    while '’' in word_list:
        word_list.remove('’')
    while '‘' in word_list:
        word_list.remove('‘')
    while '“' in word_list:
        word_list.remove('“')
    while '”' in word_list:
        word_list.remove('”')
    return word_list


def my_stopwords():
    words = [
        'would',
        'said',
        'one',
        'new',
        'also',
        'read',
        'time',
        'people',
        'says',
        'like',
        'share',
        'us',
        'years',
        'within',
        'with',
        'called',
        'asked',
        'about',
        'each',
        'mine',
        'back',
        'way',
        'always',
        'still',
        'groups',
        'put',
        'week',
        'get',
        'yet',
        'could',
        'got'
    ]
    return words


