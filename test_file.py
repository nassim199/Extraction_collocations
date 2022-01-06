from document import Document, Tweet
from requete import Requete, RequeteArxiv
import math 
#from corpus import Corpus
'''
documents = Tweet.load_documents("tweets.csv")

corpus = Corpus(documents, min_word_frequency=25, min_cooc_frequency=20)
corpus.build_vocab()
corpus.build_graph()

g = corpus.graph

#print(corpus.id_to_vocab)
#print(g.nodes())


#c = list(community.k_clique_communities(g, 2))
c = list(community.greedy_modularity_communities(g, weight='weight'))

print(len(c))'''

def build_vocab(docs):
    temp_vocab = {}
    i = 0
    for d in docs :
        text = d.text
        replacements = (',', '-', '!', '?', '.', ':', ';', '\n')
        for r in replacements:
            text = text.replace(r, ' ')
        words = text.split(" ")
        prev_i = -1
        bi_grams = {}
        for pos, w in enumerate(words):
            #if w is stop word then continue
            if w in temp_vocab:
                temp_vocab[w] = (temp_vocab[w][0]+1, temp_vocab[w][1], temp_vocab[w][2])
                temp_vocab[w][1].append(d.id)
            else:
                temp_vocab[w] = (1, [d.id], i)
                i += 1
            if prev_i != -1:
                if (prev_i, temp_vocab[w][2]) in bi_grams:
                    bi_grams[(prev_i, temp_vocab[w][2])] += 1
                else:
                    bi_grams[(prev_i, temp_vocab[w][2])] = 1
                    
            prev_i = temp_vocab[w][2]
            
    id_to_vocab = {v[2]:k for (k,v) in temp_vocab.items()}
    return temp_vocab, id_to_vocab, bi_grams


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


req = RequeteArxiv('deep+learning')    
#req = Requete("test")      
docs = req.get_documents()
#docs = Tweet.load_documents("tweets.csv")
corpus_length = len(docs)

vocab, id_to_vocab, bi_grams = build_vocab(docs)

pmis = []
for (k1, k2), cooc in bi_grams.items():
    w1 = vocab[id_to_vocab[k1]]
    w2 = vocab[id_to_vocab[k2]]
    p = pmi(w1, w2, cooc, corpus_length)
    pmis.append((w1[2], w2[2], p))
        
pmis.sort(key=lambda p: p[2], reverse=True)

bigrams = [id_to_vocab[w1] + " " + id_to_vocab[w2] + " " + str(p) for w1, w2, p in pmis]
print(bigrams[:5])        
        