from document import Document, Tweet, Arxiv
import snscrape.modules.twitter as sntwitter
import urllib, urllib.request
import xmltodict



class Requete:
    def __init__(self, content):
        self.content = content

        
        self.limit = 100 # limite les requetes a 100 documents
        
    def get_documents(self):
        pass
    
    def get_requete():
        #chacun des api a besoin d'une chaine speciale pour la recherche
        pass

class RequeteTwitter(Requete):
    
    def get_requete(self):
        req = self.content
            
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
        
        url = self.get_requete()
        data = urllib.request.urlopen(url)

        # Format dict (OrderedDict)
        data = xmltodict.parse(data.read().decode('utf-8'))  # Note : si on précise pas utf-8, le code va buguer lorsqu'il tombera sur un accent
        
        docs = []
        for i, entry in enumerate(data["feed"]["entry"]):
            docs.append(Arxiv(entry['id'], entry['summary'], entry['title'], entry['link'], entry['published']))
            
        return docs
    
def get_documents_sample():
    #ceci est une foction qui retourne une liste generique de documents 
    documents = [
        Document(1, 'I have something for you'),
        Document(2, 'the sun is shining today'),
        Document(3, 'I have better projects for the future'),
        Document(4, 'the weather is good today and the sun')
        ]
    return documents