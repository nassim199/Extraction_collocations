import networkx as nx
import random
from networkx.algorithms import community
from nltk.corpus import stopwords

import nltk
nltk.download('stopwords')

class Corpus:
    def __init__(self, docs):
        self.docs = docs
        self.graph = nx.Graph()
        self.vocab = {}
        self.id_to_vocab = {}
        self.bi_grams_cooc = {}
        
    def build_vocab(self):
        vocab = {}
        bi_grams = {}
        
        #i est utilise pour affecter des ids uniques aux mots 
        #a chaque ajout de nouveau mot on l'incremente
        i = 0
        
        for d in self.docs :
            #pour chaque document dans le corpus
            #on extrait le texte
            text = d.text
            
            #on remplace les caracteres speciaux suivants par des espaces
            replacements = (',', '-', '!', '?', '.', ':', ';', '\n')
            for r in replacements:
                text = text.replace(r, ' ')
                
            #on fait split au document selon l'espace pour avoir la liste des mots
            words = text.split(" ")
            #prev_i represente le mot precedent lu dans le document lors du parcours des mots
            prev_i = -1
            
            for pos, w in enumerate(words):
                #pour chaque mot dans la liste
                #on ignore la chaine vide
                if w == '':
                    continue
                
                if w in vocab:
                    #si le mot existe dans le vocabulaire on le met a jour
                    #on incremente le count et on ajoute l'ID du document a la listes des documents 
                    #ou il apparait
                    vocab[w] = (vocab[w][0]+1, vocab[w][1], vocab[w][2])
                    vocab[w][1].append(d.id)
                else:
                    #sinon on l'ajoute au vocab avec count = 1, liste des docs = document courant, id du mot
                    vocab[w] = (1, [d.id], i)
                    i += 1
                    
                if prev_i != -1:
                    #si ce n'est pas le premier mot qu'on lit
                    
                    # (prev_i, vocab[w][2]) est la paire de mots successives qui se suivent
                    if (prev_i, vocab[w][2]) in bi_grams:
                        #si la paire existe deja dans bi_grams alors on l'incremente le nombre de coocurrences
                        bi_grams[(prev_i, vocab[w][2])] += 1
                    else:
                        #sinon on l'initialise a 1
                        bi_grams[(prev_i, vocab[w][2])] = 1
                #on met a jour prev_i a l'ID du mot courant       
                prev_i = vocab[w][2]
                
            
        self.vocab = vocab        
        # id_to_vocab est un dictionnaire d'id vers le mot
        self.id_to_vocab = {v[2]:k for (k,v) in vocab.items()}
        
        self.bi_grams_cooc = bi_grams
        self.max_weight = 0
        
        
    def build_graph(self, max_nodes = 10):
        #on instancie le dictionnaire des stop_words
        STOP_WORDS = stopwords.words()
        
        #on filtre le vocabulaire des stop words
        vocab_without_stop_words = {k:v for (k,v) in self.vocab.items() if k not in STOP_WORDS}
        #on ordonne la liste des mots selon le nombre d'apparition
        word_counts = [v[0] for v in vocab_without_stop_words.values()]
        word_counts.sort(reverse=True)
        #afin d'extraire ensuite la frenquence minimale d'un noeud pour pouvoir l'ajouter au graphe
        min_word_frequency = word_counts[min(max_nodes, len(word_counts)-1)]
        
        #filtrer le vocabulaire selon la frequence du mot minimale de son apparation 
        #afin d'avoir que les N premiers tels que N = max_nodes
        graph_vocab = {k:v for (k,v) in vocab_without_stop_words.items() if v[0] >= min_word_frequency }
        
        
        self.graph = nx.Graph()
        
        for w, v in graph_vocab.items():
            #pour chaque mot on l'ajoute dans le graphe
            self.graph.add_nodes_from([(v[2], {"text": w, "count": v[0]})])
            
        for i, (w, v) in enumerate(list(graph_vocab.items())):
            
            for w2, v2 in list(graph_vocab.items())[i:]:
                
                #pour chaque pair possible de mots:
                #on calcule l'ensemble d'intersection
                inter = intersection(v[1], v2[1])
                
                #on calcule le score comme explique dans le rapport
                score = len(inter) / min(v[0], v2[0])
                
                #la liste des seuils qui va dependre du nombre de noeuds
                min_score = [0.3, 0.5, 0.7, 0.8, 0.8]
                
                if (score > min_score[int(max_nodes/10 - 1)]):
                    #si le score depasse le seuil on ajoute l'arete entre les deux mots
                    
                    #max_weight est le poids maximal dans le graphe on l'utilisera lors de l'affichage du graphe
                    self.max_weight = max(self.max_weight, len(inter))
                    
                    self.graph.add_edge(v[2], v2[2], weight=len(inter))
                    
    def find_communities(self):
        #on extrait la liste des communautes en utilisant l'algorithme greedy_modularity_communities de networkx
        self.communities = list(community.greedy_modularity_communities(self.graph, weight='weight'))
        self.num_communities = len(self.communities)
        
        #on genere une liste de couleurs aleatoires selon le nombre de communautes    
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                     for i in range(self.num_communities)]
        
        for colorIndex, comm in enumerate(self.communities):
            #pour chaque communaute
            c = list(comm)
            for n in c:
                #on parcourt les noeuds de la communaute courante
                #on affecte a ce noeud la couleur de de la communaute courante
                self.graph.nodes()[n]['color'] = color[colorIndex]
                
    def find_expressions(self, num_expressions = 10):
        
        corpus_length = len(self.docs)
        
        pmis = []
        for (k1, k2), cooc in self.bi_grams_cooc.items():
            #pour chaque paire dans bi_grams_cooc, pour chaque paire on a le nombre de coocurence
            
            #on extrait les mots dans vocab des deux mots a partir de leur ID
            w1 = self.vocab[self.id_to_vocab[k1]]
            w2 = self.vocab[self.id_to_vocab[k2]]
            
            #on calcule le score pmi
            p = pmi(w1, w2, cooc, corpus_length)
            
            #on ajoute les deux mots a la liste, avec son score pmi
            pmis.append((self.id_to_vocab[k1] + " " + self.id_to_vocab[k2], p))
               
        #on ordonne
        pmis.sort(key=lambda p: p[1], reverse=True)

        #on extrait seulement les N premiers
        pmis = pmis[:min(num_expressions, len(pmis))]
        
        #on retourne la liste des expressions trouves
        return [exp for exp, p in pmis]
                
                
#https://www.geeksforgeeks.org/python-intersection-two-lists/
def intersection(lst1, lst2):
    # intersection de 2 listes
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3

def pmi(w1, w2, cooc, corpus_length):
    #calcul de score pmi
    #il est a noter que dans notre cas on n'applique la fonction log mais ca ne change rien au resultat vu qu'on s'interesse au tri du score et le Log est une fonction croissante

    #chacun des mots doit apparaitre au moins 2 fois dans le corpus
    if w1[0] < 2:
        return 0
    p_w1 = w1[0] / corpus_length
    
    if w2[0] < 2:
        return 0
    p_w2 = w2[0] / corpus_length
    
    p_w1_w2 = cooc / corpus_length

    
    return p_w1_w2/(p_w1*p_w2)