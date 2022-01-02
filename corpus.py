import networkx as nx

class Corpus:
    def __init__(self, tweets):
        self.tweets = tweets
        self.graph = nx.Graph()
        self.vocab = {}
        self.id_to_vocab = {}
        self.min_word_frequency = 10
        self.min_cooc_frequency = 10
        
    def build_vocab(self):
        temp_vocab = {}
        i = 1
        for t in self.tweets:
            text = t.text
            words = text.split(" ")
            for w in words:
                if w in temp_vocab:
                    temp_vocab[w] = (temp_vocab[w][0]+1, temp_vocab[w][1], temp_vocab[w][2])
                    temp_vocab[w][1].append(t.id)
                else:
                    temp_vocab[w] = (1, [t.id], i)
                    i += 1
        self.vocab = {k: v for (k,v) in temp_vocab.items() if v[0] >= self.min_word_frequency}
        self.id_to_vocab = {v[2]: k for (k,v) in self.vocab.items()}
        
        self.max_weight = 0
        
    def build_graph(self):
        i = 0
        for k in list(self.id_to_vocab.keys()):
            i += 1
            j = i
            w = self.id_to_vocab[k]
            v = self.vocab[w]
            for k2 in list(self.id_to_vocab.keys())[i:]:
                w2 = self.id_to_vocab[k2]
                v2 = self.vocab[w2]
                j += 1
                inter = set(v[1]).intersection(set(v2[1]))
                if (len(inter) > self.min_cooc_frequency):
                    self.max_weight = max(self.max_weight, len(inter))
                    self.graph.add_edge(i, j, weight=len(inter))
                
                
