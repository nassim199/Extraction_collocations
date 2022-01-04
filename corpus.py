import networkx as nx
import random
from networkx.algorithms import community
from nltk.corpus import stopwords
#import nltk
#nltk.download('stopwords')
class Corpus:
    def __init__(self, docs, min_word_frequency = 10, min_cooc_frequency = 5):
        self.docs = docs
        self.graph = nx.Graph()
        self.vocab = {}
        self.id_to_vocab = {}
        self.min_word_frequency = min_word_frequency
        self.min_cooc_frequency = min_cooc_frequency
        self.max_nodes = 30
        
        
    def build_vocab(self):
        STOP_WORDS = stopwords.words()
        temp_vocab = {}
        i = 1
        for d in self.docs :
            text = d.text
            replacements = (',', '-', '!', '?', '.', ':', ';')
            for r in replacements:
                text = text.replace(r, ' ')
            words = text.split(" ")
            for w in words :
                #pre-processing verification
                if  w in STOP_WORDS :
                    continue
                #if w is stop word then continue
                if w in temp_vocab:
                    temp_vocab[w] = (temp_vocab[w][0]+1, temp_vocab[w][1], temp_vocab[w][2])
                    temp_vocab[w][1].append(d.id)
                else:
                    temp_vocab[w] = (1, [d.id], i)
                    i += 1
               
        word_counts = [v[0] for v in temp_vocab.values()]
        word_counts.sort(reverse=True)
        self.min_word_frequency = word_counts[min(self.max_nodes, len(word_counts)-1)]
        self.vocab = {k: v for (k,v) in temp_vocab.items() if v[0] >= self.min_word_frequency}
        self.id_to_vocab = {v[2]: k for (k,v) in self.vocab.items()}
        
        self.max_weight = 0
        
    def build_graph(self):
        
        self.min_cooc_frequency = self.min_word_frequency / 1.5
        
        for w, v in self.vocab.items():
            self.graph.add_nodes_from([(v[2], {"text": w, "count": v[0]})])
            
        for i, k in enumerate(list(self.id_to_vocab.keys())):
            w = self.id_to_vocab[k]
            v = self.vocab[w]
            for k2 in list(self.id_to_vocab.keys())[i:]:
                w2 = self.id_to_vocab[k2]
                v2 = self.vocab[w2]
                inter = set(v[1]).intersection(set(v2[1]))
                if (len(inter) > self.min_cooc_frequency):
                    self.max_weight = max(self.max_weight, len(inter))
                    self.graph.add_nodes_from([
                        (k, {"text": w, "count": v[0]}),
                        (k2, {"text": w2, "count": v2[0]})
                        ])
                    self.graph.add_edge(k, k2, weight=len(inter))
                    
    def find_communities(self):
        self.communities = list(community.greedy_modularity_communities(self.graph, weight='weight'))
        self.num_communities = len(self.communities)
        
        
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                     for i in range(self.num_communities)]
        
        for colorIndex, comm in enumerate(self.communities):
            c = list(comm)
            for n in c:
                self.graph.nodes()[n]['color'] = color[colorIndex]
            
                
                
