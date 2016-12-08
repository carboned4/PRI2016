from urllib2 import urlopen
import urlparse
import re
import time

bolas = "https://tecnico.ulisboa.pt/pt/"

site = urlopen(bolas)
content = site.read()
site.close()

linksre = '<a\s.*?href=[\'"](.*?)[\'"].*?</a>'
links = re.findall(linksre, content, re.I)
print links

queue = links
ilink = 0
visited = dict()
visited[bolas] = True

while ilink < len(queue):
    if ilink == 100:
        break
    print str(ilink) + "/" + str(len(queue)) + " : " + queue[ilink]
    if queue[ilink] in visited:
        ilink+=1
        continue
    
    time.sleep(1)
    
    url = urlparse.urljoin(bolas, queue[ilink])
    print url
    site = urlopen(url)
    content = site.read()
    
    site.close()
    visited[queue[ilink]] = True
    
    newlinks = re.findall(linksre, content, re.I)
    newnewlinks = list()
    for nl in newlinks:
        if not nl in visited:
            newnewlinks += [nl]
    queue+=newnewlinks
    ilink+=1
    