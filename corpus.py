import networkx as nx
import random
from networkx.algorithms import community
from nltk.corpus import stopwords
#import nltk
#nltk.download('stopwords')

class Corpus:
    def __init__(self, docs):
        self.docs = docs
        self.graph = nx.Graph()
        self.vocab = {}
        self.id_to_vocab = {}
        self.bi_grams_cooc = {}
        
    def build_vocab(self):
        vocab = {}
        i = 0
        for d in self.docs :
            text = d.text
            replacements = (',', '-', '!', '?', '.', ':', ';', '\n')
            for r in replacements:
                text = text.replace(r, ' ')
            words = text.split(" ")
            prev_i = -1
            bi_grams = {}
            for pos, w in enumerate(words):
                if w == '' or w == 'https' or w == '//t':
                    continue
                if w in vocab:
                    vocab[w] = (vocab[w][0]+1, vocab[w][1], vocab[w][2])
                    vocab[w][1].append(d.id)
                else:
                    vocab[w] = (1, [d.id], i)
                    i += 1
                    
                if prev_i != -1:
                    if (prev_i, vocab[w][2]) in bi_grams:
                        bi_grams[(prev_i, vocab[w][2])] += 1
                    else:
                        bi_grams[(prev_i, vocab[w][2])] = 1
                        
                prev_i = vocab[w][2]
                
            
        self.vocab = vocab        
        self.id_to_vocab = {v[2]:k for (k,v) in vocab.items()}
        
        self.bi_grams_cooc = bi_grams
        self.max_weight = 0
        
        
    def build_graph(self, max_nodes = 10):
        STOP_WORDS = stopwords.words()
        
        vocab_without_stop_words = {k:v for (k,v) in self.vocab.items() if k not in STOP_WORDS}
        word_counts = [v[0] for v in vocab_without_stop_words.values()]
        word_counts.sort(reverse=True)
        min_word_frequency = word_counts[min(max_nodes, len(word_counts)-1)]
        
        graph_vocab = {k:v for (k,v) in vocab_without_stop_words.items() if v[0] >= min_word_frequency }
        
        
        self.graph = nx.Graph()
        
        for w, v in graph_vocab.items():
            self.graph.add_nodes_from([(v[2], {"text": w, "count": v[0]})])
            
        for i, (w, v) in enumerate(list(graph_vocab.items())):
            
            for w2, v2 in list(graph_vocab.items())[i:]:
                
                inter = intersection(v[1], v2[1])
                
                score = len(inter) / min(v[0], v2[0])
                min_score = [0.3, 0.5, 0.7, 0.8, 0.9]
                
                if (score > min_score[int(max_nodes/10 - 1)]):
                    
                    self.max_weight = max(self.max_weight, len(inter))
                    
                    self.graph.add_edge(v[2], v2[2], weight=len(inter))
                    
    def find_communities(self):
        self.communities = list(community.greedy_modularity_communities(self.graph, weight='weight'))
        self.num_communities = len(self.communities)
        
        
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                     for i in range(self.num_communities)]
        
        for colorIndex, comm in enumerate(self.communities):
            c = list(comm)
            for n in c:
                self.graph.nodes()[n]['color'] = color[colorIndex]
                
    def find_expressions(self, num_expressions = 10):
        corpus_length = len(self.docs)
        
        pmis = []
        for (k1, k2), cooc in self.bi_grams_cooc.items():
            w1 = self.vocab[self.id_to_vocab[k1]]
            w2 = self.vocab[self.id_to_vocab[k2]]
            p = pmi(w1, w2, cooc, corpus_length)
            pmis.append((self.id_to_vocab[k1] + " " + self.id_to_vocab[k2], p))
                
        pmis.sort(key=lambda p: p[1], reverse=True)

        pmis = pmis[:min(num_expressions, len(pmis))]
        
        return [exp for exp, p in pmis]
                
                
#https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2):
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

def pmi(w1, w2, cooc, corpus_length):
    if w1[0] < 3:
        return 0
    p_w1 = w1[0] / corpus_length
    
    if w2[0] < 3:
        return 0
    p_w2 = w2[0] / corpus_length
    
    p_w1_w2 = cooc / corpus_length

    
    return p_w1_w2/(p_w1*p_w2)