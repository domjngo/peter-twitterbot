import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from collections import defaultdict
from heapq import nlargest


def get_url(text):
    print(text)
    url = re.search("(?P<url>https?://[^\s]+)", text).group("url")
    if url:
        print(url)
        return url
    return False


def get_article(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    article = soup.find('article')
    article = article.get_text()
    if article:
        article = article.replace('\n', ' ')
        article = re.sub('\s+', ' ', article).strip()
        return article
    return False


def summarize_article(url):
    article = get_article(url)
    sentences = sent_tokenize(article)
    sentences = list(set(sentences))
    sentences = [x for x in sentences if len(x) < 220]
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
    print(summary[0])
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

summarize_article('https://www.theguardian.com/commentisfree/2018/jun/06/labour-problem-soft-brexit-immigration-eea-government')
