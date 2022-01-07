from document import Document, Tweet
from requete import Requete, RequeteArxiv, RequeteTwitter, get_documents_sample
import math 
from corpus import Corpus
from networkx.algorithms import community

'''
#recuperation donnees twitter

req = RequeteTwitter("machine-learning")

documents = req.get_documents()

for i, doc in enumerate(documents):
    print(doc.text)
    
    print('\n--------------\n')
    if i >= 4:
        break
    

#recuperation donnees arxiv
req = RequeteArxiv("machine+learning")

documents = req.get_documents()

for i, doc in enumerate(documents):
    print(doc.text)
    
    print('\n--------------\n')
    if i >= 4:
        break
    
'''

#documents generiques pour faire des tests
docs = get_documents_sample()

#construction du vocabulaire
corpus = Corpus(docs)
corpus.build_vocab()

vocab = corpus.vocab

#affichage des mots du vocabulaire 
for k, v in vocab.items():
    print("mot : " + k)
    print("ids des documents d'apparition: ")
    print(v[1])
    print('---------')
    
id_to_vocab = corpus.id_to_vocab
bi_grams_cooc = corpus.bi_grams_cooc

for (k1, k2), cooc in bi_grams_cooc.items():
    w1 = id_to_vocab[k1]
    w2 = id_to_vocab[k2]
    
    print(w1 + " - " + w2 + " : " + str(cooc))
    
#construciton du graphe
corpus.build_graph()

g = corpus.graph
print()
print(g)

communities = list(community.greedy_modularity_communities(g, weight='weight'))
num_communities = len(communities)
print()
print("nombre de communautes : " + str(num_communities))

print("ID des mots de chaque communaute : ")
for colorIndex, comm in enumerate(communities):
    c = list(comm)
    print(c)
    
print()
expressions = corpus.find_expressions()
for exp in expressions:
    print(exp)
    print('------------')
    

