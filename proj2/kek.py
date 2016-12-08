"""
from lxml import etree
import urllib2
import xml.etree.ElementTree as ET
import codecs

file=urllib2.urlopen("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml")
#etdread = codecs.open(file,'r','utf-8')
etdread = file.read()
#etdread = etdread.decode('utf-8')
#etdread1 = etdread.encode('cp850', errors='replace')
#etdread2 = etdread1.decode('utf-8')

#root = ET.ElementTree(file=urllib2.urlopen("http://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml"))
#root = ET.parse(file=urllib2.urlopen("http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"))
root = ET.fromstring(etdread)
for elem in root.findall('.//item//*'):
    #if elem.attrib.get('name') == 'foo': print ( elem.text )
    if elem.text is not None:
        print elem.text.encode('cp850', errors='replace')

#root = etree.Element("root")
#print root.xpath(".//Airport")
"""


itemsassentences = list()
import lxml.etree as etree
#doc = etree.parse('AirFlightsData.xml')
doc = etree.parse('http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml')
for item in doc.xpath('/rss/channel/item'):
    #restitle = item.xpath('/item/title')
    restitle = item.find('title').text
    resdescription = item.find('description').text
    #print etree.tostring(item)
    print restitle.encode('cp850', errors='replace')
    print resdescription.encode('cp850', errors='replace')
    print "\n"
    #print "title " + restitle.text.encode('cp850', errors='replace')
    #for resdescription in res.xpath('//description'):
        #print resdescription.text.encode('cp850', errors='replace')
        #if resdescription.text is not None:
            #print "desc " + resdescription.text.encode('cp850', errors='replace')
#doc.freeDoc()
