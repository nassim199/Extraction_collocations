from document import Document, Tweet
from corpus import Corpus
from networkx.algorithms import community
'''
documents = Document.get_documents(None)
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

# =============== 1.2 : ArXiv ===============
# Libraries
import urllib, urllib.request, _collections
import xmltodict

# Paramètres
query_terms = ["machine", "learning"]
max_results = 50

# Requête
## Note : les f-string permettent de combiner facilement texte et variables.
## Il suffit d'écrire un f avant les "" ou '', puis d'écrire les variables directement dans la chaîne de caractères entre crochets {}
url = f'http://export.arxiv.org/api/query?search_query=all:{"+".join(query_terms)}&start=0&max_results={max_results}'
data = urllib.request.urlopen(url)

# Format dict (OrderedDict)
data = xmltodict.parse(data.read().decode('utf-8'))  # Note : si on précise pas utf-8, le code va buguer lorsqu'il tombera sur un accent

#showDictStruct(data)
docs = []
limit = 50

# Ajout titres aux docs
for i, entry in enumerate(data["feed"]["entry"]):
    if i == 0:
        print(entry.keys())
        print()
    if i%10==0: print("ArXiv:", i, "/", limit)
    docs.append(entry["title"].replace("\n", ""))

# =============== 1.3 : Exploitation ===============
print(f"# docs avec doublons : {len(docs)}")
docs = list(set(docs))
print(f"# docs sans doublons : {len(docs)}")

for i, doc in enumerate(docs):
    print(f"Document {i}\t# caractères : {len(doc)}\t# mots : {len(doc.split(' '))}\t# phrases : {len(doc.split('.'))}")
    if len(doc)<100:
        docs.remove(doc)