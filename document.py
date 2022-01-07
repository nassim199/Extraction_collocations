
import pandas as pd

class Document:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        
    @staticmethod
    def save_documents(docs, file_path):
        #cette methode sert a sauvegarder une liste de documents dans un fichier csv
        df = pd.DataFrame([[d.id, d.text] for d in docs], columns=['id', 'text'])
        df.to_csv(file_path)
    
    @staticmethod
    def load_documents(file_path):
        #cette fonction sert a charger le fichier et retourner la liste des documents
        df = pd.read_csv(file_path)
        return list(df.apply(lambda d: Document(d['id'], d['text']), axis=1))
       

class Tweet(Document):
    def __init__(self, id, text, url, date, lang):
        super().__init__(id, text)
        self.url = url
        self.date = date
        self.lang = lang

       
    
class Arxiv(Document):
    def __init__(self, id, text, title, url, date):
        super().__init__(id, text)
        self.title = title
        self.url = url
        self.date = date
