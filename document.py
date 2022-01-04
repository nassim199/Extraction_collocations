
import pandas as pd

class Document:
    def __init__(self, id, text):
        self.id = id
        self.text = text
    
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
    def save_documents(tweets, file_path):
        df = pd.DataFrame([[t.id, t.text, t.url, t.date, t.lang] for t in tweets], columns=['id', 'text', 'url', 'date', 'lang'])
        df.to_csv(file_path)
    
    @staticmethod
    def load_documents(file_path):
        df = pd.read_csv(file_path)
        return list(df.apply(lambda t: Tweet(t['id'], t['text'], t['url'], t['date'], t['lang']), axis=1))
    
    
class Arxiv(Document):
    def __init__(self, id, text, title, url, date):
        super().__init__(id, text)
        self.title = title
        self.url = url
        self.date = date
