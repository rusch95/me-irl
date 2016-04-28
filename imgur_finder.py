import bz2
import json
import urllib2
import re

path = '/home/rusch/Projects/reddit_data/2012/RC_2012-01.bz2'
f = bz2.BZ2File(path)
repeats = {}
removed = {}

for line in f:
    body = json.loads(line)['body']
    if body.find('imgur.com') != -1:
        try:
            url = re.search("(?P<url>https?://i?.?imgur[^\s\)]+.gifv?)", body).group("url")
            if len(url) == 28 and (not url[19:25] in repeats and not url[19:25] in removed):
                try:
                    req = urllib2.Request(url)
                    res = urllib2.urlopen(req)
                    final = res.geturl()
                    tag = url[19:25]
                    if final.find('removed') == -1:
                        print final
                        repeats[tag] = final
                    else:
                        removed[tag] = None
                except urllib2.HTTPError:
                    pass



            elif len(url) == 28:
                tag = url[19:25]
                print repeats[tag]



            else:
                try:
                    req = urllib2.Request(url)
                    res = urllib2.urlopen(req)
                    final = res.geturl()
                    if final.find('removed') == -1:
                        print final
                except urllib2.HTTPError:
                    pass

        except AttributeError:
            pass

