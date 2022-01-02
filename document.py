import snscrape.modules.twitter as sntwitter

class Tweet:
    def __init__(self, id, text, url, date, lang):
        self.id = id
        self.text = text
        self.url = url
        self.date = date
        self.lang = lang
        
    @staticmethod
    def get_tweets(requete):
        tweets = []
        #for i, t in enumerate(sntwitter.TwitterSearchScraper(requete.get_requete()).get_items()):
        #    tweets.append(Tweet(t.id, t.content, t.url, t.date, t.lang))
            
        tweets = [
            Tweet(1, 'I have something for you', '', '', ''),
            Tweet(2, 'The sun is shining today', '', '', ''),
            Tweet(3, 'I have better projects for the future', '', '', ''),
            Tweet(4, 'the weather is good today', '', '', '')
            ]
            
        return tweets