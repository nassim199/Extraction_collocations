def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class Requete:
    def __init__(self, content, lang='', user='', city='', radius='', since='', until=''):
        self.content = content
        self.lang = lang
        self.user = user
        self.city = city
        self.radius = radius
        self.since = since 
        self.until = until
    
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