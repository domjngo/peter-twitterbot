from __future__ import with_statement

import feedparser
import link


def contains_wanted(query, in_str):
    query = query.split()
    i = 0
    for wrd in query:
        if wrd.lower() in in_str:
            n = in_str.lower().split().count(wrd.lower())
            i += n
    return i


def search_guides(query):
    rss = 'data.xml'
    feed = feedparser.parse(rss)
    results = []
    n = 0

    for key in feed["entries"]:
        url = key['link'].replace('livelb', 'www')
        title = key['title']
        content = key['content'][0]['value']
        c = contains_wanted(query, content.lower())
        t = contains_wanted(query, title.lower())
        i = c + (t*3)

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

