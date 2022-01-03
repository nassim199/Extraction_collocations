import snscrape.modules.twitter as sntwitter
import pandas as pd

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
    
    @staticmethod
    def save_documents(file_path):
        pass
    
    @staticmethod
    def load_documents(file_path):
        pass        

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
    
    @staticmethod
    def save_documents(tweets, file_path):
        df = pd.DataFrame([[t.id, t.text, t.url, t.date, t.lang] for t in tweets], columns=['id', 'text', 'url', 'date', 'lang'])
        df.to_csv(file_path)
    
    @staticmethod
    def load_documents(file_path):
        df = pd.read_csv(file_path)
        return list(df.apply(lambda t: Tweet(t['id'], t['text'], t['url'], t['date'], t['lang']), axis=1))