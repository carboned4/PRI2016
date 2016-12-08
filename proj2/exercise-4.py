from urllib2 import urlopen
site = urlopen("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")
content = site.read()
site.close()

import re
linksre = '<a\s.*?href=[\'"](.*?)[\'"].*?</a>'
links = re.findall(linksre, content, re.I)
print links