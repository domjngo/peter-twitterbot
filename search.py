from __future__ import with_statement

import feedparser
import link
from nltk.corpus import stopwords


def remove_stop_words(text):
    stop_words = stopwords.words("english")
    return ' '.join([word for word in text.split() if word not in stop_words])


def contains_wanted(query, in_str):
    query = query.split()
    i = 0
    for wrd in query:
        if wrd.lower() in in_str:
            n = in_str.lower().split().count(wrd.lower())
            i += n
    return i


def search_guides(query):
    query = remove_stop_words(query)
    rss = 'data.xml'
    feed = feedparser.parse(rss)
    results = []
    n = 0

    for key in feed["entries"]:
        url = key['link'].replace('livelb', 'www')
        title = key['title']
        content = key['content'][0]['value']
        cat = [t.term for t in key.get('tags', [])]
        if 'Help with your research' in cat:
            cat.remove('Help with your research')
        print(cat)
        categories = ' '.join(cat)
        c = contains_wanted(query, content.lower())
        t = contains_wanted(query, title.lower())
        g = contains_wanted(query, categories.lower())
        i = c + (t*3) + (g*3)

        if i > 0:
            result = '{} - {} - {}'.format(i, title, url)
            print(result)

            row = []
            row.append(i)
            row.append(title)
            row.append(url)
            results.append(row)

            n += 1

    if results:
        top_result = max(results, key=lambda x: x[0])
        guide = top_result[1]
        guide_url = link.make_tiny(top_result[2])
        print('{} {}'.format(guide, guide_url))
        return '{} {}'.format(guide, guide_url)

    return False

