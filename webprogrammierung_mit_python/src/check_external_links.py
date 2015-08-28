from HTMLParser import HTMLParser
from urllib2 import urlopen
import sys



class LinksExtractor(HTMLParser): # derive new HTML parser

    def __init__(self) :        # class constructor
        HTMLParser.__init__(self)  # base class constructor
        self.links = []        # create an empty list for storing hyperlinks

    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        else:
            if len(attrs) > 0 :
                for attr in attrs :
                    if attr[0] == "href" :         # ignore all non HREF attributes
                        self.links.append(attr[1])
            
        
    def get_links(self) :     # return the list of extracted links
        return self.links
    

htmlparser = LinksExtractor() 

endpoint = "http://www.tigerjython.ch/index.php?inhalt_links=navigation.inc.php&inhalt_mitte=anhang/links.inc.php"  
#endpoint = "http://www.tigerjython.ch/index.php?inhalt_links=navigation.inc.php&inhalt_mitte=internet/search.inc.php"

response = urlopen(endpoint)
html = response.read()
response.close()

encodedhtml=unicode(html, 'iso-8859-1')
htmlparser.feed(encodedhtml)      # parse the file saving the info about links
htmlparser.close()
links = htmlparser.get_links()   # get the hyperlinks list

# Color String
CSI="\x1B["

#links=["http://www.unibas.ch","http://www.blick.ch","http://www.basel.ch"]

for link in links:
    s = link[:7]
    if s.lower() == 'http://':
        try:
            conn = urlopen(link,timeout=3)
            code = conn.getcode()
            msg = conn.msg
            conn.close()
            if code != 200:
                print CSI+"30;45m" + msg + " " + link +  CSI + "0m"+"\n"
            else:
                print CSI+"30;42m" +"OK: "+CSI+"30;42m"+ link + CSI + "0m"+"\n"
        except:
            print  CSI+"30;45m" + "could not connect " + link +   CSI + "0m"+"\n"
        
        sys.stdout.flush()
                
"END"