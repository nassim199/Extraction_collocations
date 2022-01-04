from document import Document, Tweet, Arxiv
import snscrape.modules.twitter as sntwitter
import urllib, urllib.request, _collections
import xmltodict



class Requete:
    def __init__(self, content, lang='', user='', city='', radius='', since='', until=''):
        self.content = content
        self.lang = lang
        self.user = user
        self.city = city
        self.radius = radius
        self.since = since 
        self.until = until
        
        self.limit = 500 # limite les requetes a 100 documents
        
    def get_documents(self):
        documents = [
            Document(1, 'I have something for you'),
            Document(2, 'the sun is shining today'),
            Document(3, 'I have better projects for the future'),
            Document(4, 'the weather is good today and the sun')
            ]
        return documents
    
    def get_requete():
        pass

class RequeteTwitter(Requete):
    
    def get_requete(self):
        req = self.content
        
        if self.lang != '':
            req += ' lang:' + self.lang
            
        if self.user != '':
            req += ' user:' + self.user
            
        if self.city != '':
            req += ' near:' + self.city
            if self.radius != '':
                req += ' within:' + self.radius + 'km'
            else:
                req += ' within:5km'
                
        if self.since != '':
            req += ' since:' + self.since
            
        if self.until != '':
            req += ' until:' + self.until
            
        return req
    
    def get_documents(self):
        tweets = []
        for i, t in enumerate(sntwitter.TwitterSearchScraper(self.get_requete()).get_items()):
            tweets.append(Tweet(t.id, t.content, t.url, t.date, t.lang))
            if i > self.limit:
                break
            
        return tweets
    
class RequeteArxiv(Requete):
    def get_requete(self):
        url = f'http://export.arxiv.org/api/query?search_query=all:{self.content}&start=0&max_results={self.limit}'
        return url
    
    def get_documents(self):
        self.limit = 50
        
        url = self.get_requete()
        data = urllib.request.urlopen(url)

        # Format dict (OrderedDict)
        data = xmltodict.parse(data.read().decode('utf-8'))  # Note : si on précise pas utf-8, le code va buguer lorsqu'il tombera sur un accent
        
        docs = []
        for i, entry in enumerate(data["feed"]["entry"]):
            docs.append(Arxiv(entry['id'], entry['summary'], entry['title'], entry['link'], entry['published']))
            
        return docs