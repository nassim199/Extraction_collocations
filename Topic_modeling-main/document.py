import snscrape.modules.twitter as sntwitter

class Document:
    def __init__(self, id, text):
        self.id = id
        self.text = text
    
    @staticmethod
    def get_documents(requete):
        documents = [
            Document(1, 'I have something for you'),
            Document(2, 'the sun is shining today'),
            Document(3, 'I have better projects for the future'),
            Document(4, 'the weather is good today and the sun')
            ]
        return documents
        

class Tweet(Document):
    def __init__(self, id, text, url, date, lang):
        super().__init__(id, text)
        self.url = url
        self.date = date
        self.lang = lang
        
    @staticmethod
    def get_documents(requete):
        tweets = []
        for i, t in enumerate(sntwitter.TwitterSearchScraper(requete.get_requete()).get_items()):
            tweets.append(Tweet(t.id, t.content, t.url, t.date, t.lang))
            
        return tweets