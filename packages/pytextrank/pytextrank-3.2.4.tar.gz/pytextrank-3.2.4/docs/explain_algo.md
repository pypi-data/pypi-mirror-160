

!!! note
    To run this notebook in JupyterLab, load [`examples/explain_algo.ipynb`](https://github.com/DerwenAI/pytextrank/blob/main/examples/explain_algo.ipynb)



# Explain PyTextRank: the algorithm

Let's look at the *TextRank* algorithm used to build a graph from a raw text, and then from that extract the top-ranked phrases. This work is based on 
["TextRank: Bringing Order into Text"](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf),
Rada Mihalcea, Paul Tarau, _Empirical Methods in Natural Language Processing_ (2004).

---
First we perform some basic housekeeping for Jupyter, then load `spaCy` with a language model for English ...


```python
import warnings
warnings.filterwarnings("ignore")
```


```python
import spacy
nlp = spacy.load("en_core_web_sm")
```

Now, to get started, we'll create some text to use.


```python
#text = "When Ada was twelve years old, this future 'Lady Fairy', as Charles Babbage affectionately called her, decided she wanted to fly. Ada Byron went about the project methodically, thoughtfully, with imagination and passion. Her first step, in February 1828, was to construct wings. She investigated different material and sizes. She considered various materials for the wings: paper, oilsilk, wires, and feathers. She examined the anatomy of birds to determine the right proportion between the wings and the body. She decided to write a book, Flyology, illustrating, with plates, some of her findings. She decided what equipment she would need; for example, a compass, to 'cut across the country by the most direct road', so that she could surmount mountains, rivers, and valleys. Her final step was to integrate steam with the 'art of flying."

text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

doc = nlp(text)
```

How many sentences are in the parsed document and where are their boundaries?


```python
from icecream import ic

for sent in doc.sents:
    ic(sent.start, sent.end)
```

    ic| sent.start: 0, sent.end: 13
    ic| sent.start: 13, sent.end: 33
    ic| sent.start: 33, sent.end: 61
    ic| sent.start: 61, sent.end: 91


What are the raw _noun chunks_ in the parsed document?


```python
for chunk in doc.noun_chunks:
    ic(chunk.text)
```

    ic| chunk.text: 'Compatibility'
    ic| chunk.text: 'systems'
    ic| chunk.text: 'linear constraints'
    ic| chunk.text: 'the set'
    ic| chunk.text: 'natural numbers'
    ic| chunk.text: 'Criteria'
    ic| chunk.text: 'compatibility'
    ic| chunk.text: 'a system'
    ic| chunk.text: 'linear Diophantine equations'
    ic| chunk.text: 'strict inequations'
    ic| chunk.text: 'nonstrict inequations'
    ic| chunk.text: 'Upper bounds'
    ic| chunk.text: 'components'
    ic| chunk.text: 'a minimal set'
    ic| chunk.text: 'solutions'
    ic| chunk.text: 'algorithms'
    ic| chunk.text: 'construction'
    ic| chunk.text: 'minimal generating sets'
    ic| chunk.text: 'solutions'
    ic| chunk.text: 'all types'
    ic| chunk.text: 'systems'
    ic| chunk.text: 'These criteria'
    ic| chunk.text: 'the corresponding algorithms'
    ic| chunk.text: 'a minimal supporting set'
    ic| chunk.text: 'solutions'
    ic| chunk.text: 'all the considered types systems'
    ic| chunk.text: 'systems'
    ic| chunk.text: 'mixed types'


Also, does `spaCy` detect any _named entities_?


```python
for ent in doc.ents:
    ic(ent.text, ent.label_, ent.start, ent.end)
```

    ic| ent.text: 'Diophantine'
        ent.label_: 'GPE'
        ent.start: 21
        ent.end: 22


Given those details about the parsed document, next we use [NetworkX](https://networkx.github.io/) to manage an in-memory graph...


```python
import networkx as nx

def increment_edge (graph, node0, node1):
    ic(node0, node1)
    
    if graph.has_edge(node0, node1):
        graph[node0][node1]["weight"] += 1.0
    else:
        graph.add_edge(node0, node1, weight=1.0)
```

Then construct a graph, sentence by sentence, based on the [spaCy part-of-speech tags](https://spacy.io/api/annotation#pos-en) tags:


```python
POS_KEPT = ["ADJ", "NOUN", "PROPN", "VERB"]

def link_sentence (doc, sent, lemma_graph, seen_lemma):
    visited_tokens = []
    visited_nodes = []

    for i in range(sent.start, sent.end):
        token = doc[i]

        if token.pos_ in POS_KEPT:
            key = (token.lemma_, token.pos_)

            if key not in seen_lemma:
                seen_lemma[key] = set([token.i])
            else:
                seen_lemma[key].add(token.i)

            node_id = list(seen_lemma.keys()).index(key)

            if not node_id in lemma_graph:
                lemma_graph.add_node(node_id)

            ic(visited_tokens, visited_nodes)
            ic(list(range(len(visited_tokens) - 1, -1, -1)))
            
            for prev_token in range(len(visited_tokens) - 1, -1, -1):
                ic(prev_token, (token.i - visited_tokens[prev_token]))
                
                if (token.i - visited_tokens[prev_token]) <= 3:
                    increment_edge(lemma_graph, node_id, visited_nodes[prev_token])
                else:
                    break

            ic(token.i, token.text, token.lemma_, token.pos_, visited_tokens, visited_nodes)

            visited_tokens.append(token.i)
            visited_nodes.append(node_id)
```

Now iterate through the sentences to construct the lemma graph...


```python
lemma_graph = nx.Graph()
seen_lemma = {}

for sent in doc.sents:
    link_sentence(doc, sent, lemma_graph, seen_lemma)
    #break # only test one sentence
```

    ic| visited_tokens: [], visited_nodes: []
    ic| list(range(len(visited_tokens) - 1, -1, -1)): []
    ic| token.i: 0
        token.text: 'Compatibility'
        token.lemma_: 'compatibility'
        token.pos_: 'NOUN'
        visited_tokens: []
        visited_nodes: []
    ic| visited_tokens: [0], visited_nodes: [0]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [0]
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 2
    ic| node0: 1, node1: 0
    ic| token.i: 2
        token.text: 'systems'
        token.lemma_: 'system'
        token.pos_: 'NOUN'
        visited_tokens: [0]
        visited_nodes: [0]
    ic| visited_tokens: [0, 2], visited_nodes: [0, 1]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [1, 0]
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 2
    ic| node0: 2, node1: 1
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 4
        token.text: 'linear'
        token.lemma_: 'linear'
        token.pos_: 'ADJ'
        visited_tokens: [0, 2]
        visited_nodes: [0, 1]
    ic| visited_tokens: [0, 2, 4], visited_nodes: [0, 1, 2]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [2, 1, 0]
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 1
    ic| node0: 3, node1: 2
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 3
    ic| node0: 3, node1: 1
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 5
        token.text: 'constraints'
        token.lemma_: 'constraint'
        token.pos_: 'NOUN'
        visited_tokens: [0, 2, 4]
        visited_nodes: [0, 1, 2]
    ic| visited_tokens: [0, 2, 4, 5], visited_nodes: [0, 1, 2, 3]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [3, 2, 1, 0]
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 3
    ic| node0: 4, node1: 3
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 8
        token.text: 'set'
        token.lemma_: 'set'
        token.pos_: 'NOUN'
        visited_tokens: [0, 2, 4, 5]
        visited_nodes: [0, 1, 2, 3]
    ic| visited_tokens: [0, 2, 4, 5, 8], visited_nodes: [0, 1, 2, 3, 4]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [4, 3, 2, 1, 0]
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 2
    ic| node0: 5, node1: 4
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 10
        token.text: 'natural'
        token.lemma_: 'natural'
        token.pos_: 'ADJ'
        visited_tokens: [0, 2, 4, 5, 8]
        visited_nodes: [0, 1, 2, 3, 4]
    ic| visited_tokens: [0, 2, 4, 5, 8, 10]
        visited_nodes: [0, 1, 2, 3, 4, 5]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [5, 4, 3, 2, 1, 0]
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 1
    ic| node0: 6, node1: 5
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 3
    ic| node0: 6, node1: 4
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 6
    ic| token.i: 11
        token.text: 'numbers'
        token.lemma_: 'number'
        token.pos_: 'NOUN'
        visited_tokens: [0, 2, 4, 5, 8, 10]
        visited_nodes: [0, 1, 2, 3, 4, 5]
    ic| visited_tokens: [], visited_nodes: []
    ic| list(range(len(visited_tokens) - 1, -1, -1)): []
    ic| token.i: 13
        token.text: 'Criteria'
        token.lemma_: 'criterion'
        token.pos_: 'NOUN'
        visited_tokens: []
        visited_nodes: []
    ic| visited_tokens: [13], visited_nodes: [7]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [0]
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 2
    ic| node0: 0, node1: 7
    ic| token.i: 15
        token.text: 'compatibility'
        token.lemma_: 'compatibility'
        token.pos_: 'NOUN'
        visited_tokens: [13]
        visited_nodes: [7]
    ic| visited_tokens: [13, 15], visited_nodes: [7, 0]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [1, 0]
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 3
    ic| node0: 1, node1: 0
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 18
        token.text: 'system'
        token.lemma_: 'system'
        token.pos_: 'NOUN'
        visited_tokens: [13, 15]
        visited_nodes: [7, 0]
    ic| visited_tokens: [13, 15, 18], visited_nodes: [7, 0, 1]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [2, 1, 0]
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 2
    ic| node0: 2, node1: 1
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 20
        token.text: 'linear'
        token.lemma_: 'linear'
        token.pos_: 'ADJ'
        visited_tokens: [13, 15, 18]
        visited_nodes: [7, 0, 1]
    ic| visited_tokens: [13, 15, 18, 20], visited_nodes: [7, 0, 1, 2]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [3, 2, 1, 0]
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 1
    ic| node0: 8, node1: 2
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 3
    ic| node0: 8, node1: 1
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 6
    ic| token.i: 21
        token.text: 'Diophantine'
        token.lemma_: 'Diophantine'
        token.pos_: 'PROPN'
        visited_tokens: [13, 15, 18, 20]
        visited_nodes: [7, 0, 1, 2]
    ic| visited_tokens: [13, 15, 18, 20, 21]
        visited_nodes: [7, 0, 1, 2, 8]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [4, 3, 2, 1, 0]
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 1
    ic| node0: 9, node1: 8
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 2
    ic| node0: 9, node1: 2
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 22
        token.text: 'equations'
        token.lemma_: 'equation'
        token.pos_: 'NOUN'
        visited_tokens: [13, 15, 18, 20, 21]
        visited_nodes: [7, 0, 1, 2, 8]
    ic| visited_tokens: [13, 15, 18, 20, 21, 22]
        visited_nodes: [7, 0, 1, 2, 8, 9]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [5, 4, 3, 2, 1, 0]
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 2
    ic| node0: 10, node1: 9
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 3
    ic| node0: 10, node1: 8
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 24
        token.text: 'strict'
        token.lemma_: 'strict'
        token.pos_: 'ADJ'
        visited_tokens: [13, 15, 18, 20, 21, 22]
        visited_nodes: [7, 0, 1, 2, 8, 9]
    ic| visited_tokens: [13, 15, 18, 20, 21, 22, 24]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 1
    ic| node0: 11, node1: 10
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 3
    ic| node0: 11, node1: 9
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 25
        token.text: 'inequations'
        token.lemma_: 'inequation'
        token.pos_: 'NOUN'
        visited_tokens: [13, 15, 18, 20, 21, 22, 24]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10]
    ic| visited_tokens: [13, 15, 18, 20, 21, 22, 24, 25]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10, 11]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 3
    ic| node0: 12, node1: 11
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 28
        token.text: 'nonstrict'
        token.lemma_: 'nonstrict'
        token.pos_: 'ADJ'
        visited_tokens: [13, 15, 18, 20, 21, 22, 24, 25]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10, 11]
    ic| visited_tokens: [13, 15, 18, 20, 21, 22, 24, 25, 28]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10, 11, 12]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 1
    ic| node0: 11, node1: 12
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 29
        token.text: 'inequations'
        token.lemma_: 'inequation'
        token.pos_: 'NOUN'
        visited_tokens: [13, 15, 18, 20, 21, 22, 24, 25, 28]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10, 11, 12]
    ic| visited_tokens: [13, 15, 18, 20, 21, 22, 24, 25, 28, 29]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10, 11, 12, 11]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 9, token.i - visited_tokens[prev_token]: 2
    ic| node0: 13, node1: 11
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 3
    ic| node0: 13, node1: 12
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 6
    ic| token.i: 31
        token.text: 'considered'
        token.lemma_: 'consider'
        token.pos_: 'VERB'
        visited_tokens: [13, 15, 18, 20, 21, 22, 24, 25, 28, 29]
        visited_nodes: [7, 0, 1, 2, 8, 9, 10, 11, 12, 11]
    ic| visited_tokens: [], visited_nodes: []
    ic| list(range(len(visited_tokens) - 1, -1, -1)): []
    ic| token.i: 33
        token.text: 'Upper'
        token.lemma_: 'Upper'
        token.pos_: 'PROPN'
        visited_tokens: []
        visited_nodes: []
    ic| visited_tokens: [33], visited_nodes: [14]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [0]
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 1
    ic| node0: 15, node1: 14
    ic| token.i: 34
        token.text: 'bounds'
        token.lemma_: 'bound'
        token.pos_: 'NOUN'
        visited_tokens: [33]
        visited_nodes: [14]
    ic| visited_tokens: [33, 34], visited_nodes: [14, 15]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [1, 0]
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 2
    ic| node0: 16, node1: 15
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 3
    ic| node0: 16, node1: 14
    ic| token.i: 36
        token.text: 'components'
        token.lemma_: 'component'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34]
        visited_nodes: [14, 15]
    ic| visited_tokens: [33, 34, 36], visited_nodes: [14, 15, 16]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [2, 1, 0]
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 3
    ic| node0: 17, node1: 16
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 39
        token.text: 'minimal'
        token.lemma_: 'minimal'
        token.pos_: 'ADJ'
        visited_tokens: [33, 34, 36]
        visited_nodes: [14, 15, 16]
    ic| visited_tokens: [33, 34, 36, 39], visited_nodes: [14, 15, 16, 17]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [3, 2, 1, 0]
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 1
    ic| node0: 4, node1: 17
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 40
        token.text: 'set'
        token.lemma_: 'set'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39]
        visited_nodes: [14, 15, 16, 17]
    ic| visited_tokens: [33, 34, 36, 39, 40]
        visited_nodes: [14, 15, 16, 17, 4]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [4, 3, 2, 1, 0]
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 2
    ic| node0: 18, node1: 4
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 3
    ic| node0: 18, node1: 17
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 6
    ic| token.i: 42
        token.text: 'solutions'
        token.lemma_: 'solution'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40]
        visited_nodes: [14, 15, 16, 17, 4]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42]
        visited_nodes: [14, 15, 16, 17, 4, 18]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [5, 4, 3, 2, 1, 0]
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 2
    ic| node0: 19, node1: 18
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 44
        token.text: 'algorithms'
        token.lemma_: 'algorithm'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42]
        visited_nodes: [14, 15, 16, 17, 4, 18]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 2
    ic| node0: 20, node1: 19
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 46
        token.text: 'construction'
        token.lemma_: 'construction'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 2
    ic| node0: 17, node1: 20
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 48
        token.text: 'minimal'
        token.lemma_: 'minimal'
        token.pos_: 'ADJ'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 1
    ic| node0: 21, node1: 17
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 3
    ic| node0: 21, node1: 20
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 49
        token.text: 'generating'
        token.lemma_: 'generating'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 9, token.i - visited_tokens[prev_token]: 1
    ic| node0: 4, node1: 21
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 2
    ic| node0: 4, node1: 17
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 50
        token.text: 'sets'
        token.lemma_: 'set'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 10, token.i - visited_tokens[prev_token]: 2
    ic| node0: 18, node1: 4
    ic| prev_token: 9, token.i - visited_tokens[prev_token]: 3
    ic| node0: 18, node1: 21
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 52
        token.text: 'solutions'
        token.lemma_: 'solution'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50, 52]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4, 18]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 11, token.i - visited_tokens[prev_token]: 3
    ic| node0: 22, node1: 18
    ic| prev_token: 10, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 55
        token.text: 'types'
        token.lemma_: 'type'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50, 52]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4, 18]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50, 52, 55]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4, 18, 22]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 12, token.i - visited_tokens[prev_token]: 2
    ic| node0: 1, node1: 22
    ic| prev_token: 11, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 57
        token.text: 'systems'
        token.lemma_: 'system'
        token.pos_: 'NOUN'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50, 52, 55]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4, 18, 22]
    ic| visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50, 52, 55, 57]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4, 18, 22, 1]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 13, token.i - visited_tokens[prev_token]: 2
    ic| node0: 23, node1: 1
    ic| prev_token: 12, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 59
        token.text: 'given'
        token.lemma_: 'give'
        token.pos_: 'VERB'
        visited_tokens: [33, 34, 36, 39, 40, 42, 44, 46, 48, 49, 50, 52, 55, 57]
        visited_nodes: [14, 15, 16, 17, 4, 18, 19, 20, 17, 21, 4, 18, 22, 1]
    ic| visited_tokens: [], visited_nodes: []
    ic| list(range(len(visited_tokens) - 1, -1, -1)): []
    ic| token.i: 62
        token.text: 'criteria'
        token.lemma_: 'criterion'
        token.pos_: 'NOUN'
        visited_tokens: []
        visited_nodes: []
    ic| visited_tokens: [62], visited_nodes: [7]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [0]
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 3
    ic| node0: 24, node1: 7
    ic| token.i: 65
        token.text: 'corresponding'
        token.lemma_: 'correspond'
        token.pos_: 'VERB'
        visited_tokens: [62]
        visited_nodes: [7]
    ic| visited_tokens: [62, 65], visited_nodes: [7, 24]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [1, 0]
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 1
    ic| node0: 19, node1: 24
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 66
        token.text: 'algorithms'
        token.lemma_: 'algorithm'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65]
        visited_nodes: [7, 24]
    ic| visited_tokens: [62, 65, 66], visited_nodes: [7, 24, 19]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [2, 1, 0]
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 2
    ic| node0: 25, node1: 19
    ic| prev_token: 1, token.i - visited_tokens[prev_token]: 3
    ic| node0: 25, node1: 24
    ic| prev_token: 0, token.i - visited_tokens[prev_token]: 6
    ic| token.i: 68
        token.text: 'constructing'
        token.lemma_: 'construct'
        token.pos_: 'VERB'
        visited_tokens: [62, 65, 66]
        visited_nodes: [7, 24, 19]
    ic| visited_tokens: [62, 65, 66, 68], visited_nodes: [7, 24, 19, 25]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [3, 2, 1, 0]
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 2
    ic| node0: 17, node1: 25
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 70
        token.text: 'minimal'
        token.lemma_: 'minimal'
        token.pos_: 'ADJ'
        visited_tokens: [62, 65, 66, 68]
        visited_nodes: [7, 24, 19, 25]
    ic| visited_tokens: [62, 65, 66, 68, 70]
        visited_nodes: [7, 24, 19, 25, 17]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [4, 3, 2, 1, 0]
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 1
    ic| node0: 26, node1: 17
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 3
    ic| node0: 26, node1: 25
    ic| prev_token: 2, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 71
        token.text: 'supporting'
        token.lemma_: 'support'
        token.pos_: 'VERB'
        visited_tokens: [62, 65, 66, 68, 70]
        visited_nodes: [7, 24, 19, 25, 17]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71]
        visited_nodes: [7, 24, 19, 25, 17, 26]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [5, 4, 3, 2, 1, 0]
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 1
    ic| node0: 4, node1: 26
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 2
    ic| node0: 4, node1: 17
    ic| prev_token: 3, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 72
        token.text: 'set'
        token.lemma_: 'set'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65, 66, 68, 70, 71]
        visited_nodes: [7, 24, 19, 25, 17, 26]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 2
    ic| node0: 18, node1: 4
    ic| prev_token: 5, token.i - visited_tokens[prev_token]: 3
    ic| node0: 18, node1: 26
    ic| prev_token: 4, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 74
        token.text: 'solutions'
        token.lemma_: 'solution'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 3
    ic| node0: 27, node1: 18
    ic| prev_token: 6, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 77
        token.text: 'used'
        token.lemma_: 'use'
        token.pos_: 'VERB'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 2
    ic| node0: 28, node1: 27
    ic| prev_token: 7, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 79
        token.text: 'solving'
        token.lemma_: 'solve'
        token.pos_: 'VERB'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 9, token.i - visited_tokens[prev_token]: 3
    ic| node0: 13, node1: 28
    ic| prev_token: 8, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 82
        token.text: 'considered'
        token.lemma_: 'consider'
        token.pos_: 'VERB'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 10, token.i - visited_tokens[prev_token]: 1
    ic| node0: 22, node1: 13
    ic| prev_token: 9, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 83
        token.text: 'types'
        token.lemma_: 'type'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 11, token.i - visited_tokens[prev_token]: 1
    ic| node0: 1, node1: 22
    ic| prev_token: 10, token.i - visited_tokens[prev_token]: 2
    ic| node0: 1, node1: 13
    ic| prev_token: 9, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 84
        token.text: 'systems'
        token.lemma_: 'system'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22, 1]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 12, token.i - visited_tokens[prev_token]: 2
    ic| node0: 1, node1: 1
    ic| prev_token: 11, token.i - visited_tokens[prev_token]: 3
    ic| node0: 1, node1: 22
    ic| prev_token: 10, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 86
        token.text: 'systems'
        token.lemma_: 'system'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22, 1]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84, 86]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22, 1, 1]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 13, token.i - visited_tokens[prev_token]: 2
    ic| node0: 29, node1: 1
    ic| prev_token: 12, token.i - visited_tokens[prev_token]: 4
    ic| token.i: 88
        token.text: 'mixed'
        token.lemma_: 'mixed'
        token.pos_: 'ADJ'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84, 86]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22, 1, 1]
    ic| visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84, 86, 88]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22, 1, 1, 29]
    ic| list(range(len(visited_tokens) - 1, -1, -1)): [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    ic| prev_token: 14, token.i - visited_tokens[prev_token]: 1
    ic| node0: 22, node1: 29
    ic| prev_token: 13, token.i - visited_tokens[prev_token]: 3
    ic| node0: 22, node1: 1
    ic| prev_token: 12, token.i - visited_tokens[prev_token]: 5
    ic| token.i: 89
        token.text: 'types'
        token.lemma_: 'type'
        token.pos_: 'NOUN'
        visited_tokens: [62, 65, 66, 68, 70, 71, 72, 74, 77, 79, 82, 83, 84, 86, 88]
        visited_nodes: [7, 24, 19, 25, 17, 26, 4, 18, 27, 28, 13, 22, 1, 1, 29]



```python
ic(seen_lemma)
```

    ic| seen_lemma: {('Diophantine', 'PROPN'): {21},
                     ('Upper', 'PROPN'): {33},
                     ('algorithm', 'NOUN'): {66, 44},
                     ('bound', 'NOUN'): {34},
                     ('compatibility', 'NOUN'): {0, 15},
                     ('component', 'NOUN'): {36},
                     ('consider', 'VERB'): {82, 31},
                     ('constraint', 'NOUN'): {5},
                     ('construct', 'VERB'): {68},
                     ('construction', 'NOUN'): {46},
                     ('correspond', 'VERB'): {65},
                     ('criterion', 'NOUN'): {13, 62},
                     ('equation', 'NOUN'): {22},
                     ('generating', 'NOUN'): {49},
                     ('give', 'VERB'): {59},
                     ('inequation', 'NOUN'): {25, 29},
                     ('linear', 'ADJ'): {4, 20},
                     ('minimal', 'ADJ'): {48, 70, 39},
                     ('mixed', 'ADJ'): {88},
                     ('natural', 'ADJ'): {10},
                     ('nonstrict', 'ADJ'): {28},
                     ('number', 'NOUN'): {11},
                     ('set', 'NOUN'): {8, 40, 72, 50},
                     ('solution', 'NOUN'): {42, 52, 74},
                     ('solve', 'VERB'): {79},
                     ('strict', 'ADJ'): {24},
                     ('support', 'VERB'): {71},
                     ('system', 'NOUN'): {2, 18, 84, 86, 57},
                     ('type', 'NOUN'): {89, 83, 55},
                     ('use', 'VERB'): {77}}





    {('compatibility', 'NOUN'): {0, 15},
     ('system', 'NOUN'): {2, 18, 57, 84, 86},
     ('linear', 'ADJ'): {4, 20},
     ('constraint', 'NOUN'): {5},
     ('set', 'NOUN'): {8, 40, 50, 72},
     ('natural', 'ADJ'): {10},
     ('number', 'NOUN'): {11},
     ('criterion', 'NOUN'): {13, 62},
     ('Diophantine', 'PROPN'): {21},
     ('equation', 'NOUN'): {22},
     ('strict', 'ADJ'): {24},
     ('inequation', 'NOUN'): {25, 29},
     ('nonstrict', 'ADJ'): {28},
     ('consider', 'VERB'): {31, 82},
     ('Upper', 'PROPN'): {33},
     ('bound', 'NOUN'): {34},
     ('component', 'NOUN'): {36},
     ('minimal', 'ADJ'): {39, 48, 70},
     ('solution', 'NOUN'): {42, 52, 74},
     ('algorithm', 'NOUN'): {44, 66},
     ('construction', 'NOUN'): {46},
     ('generating', 'NOUN'): {49},
     ('type', 'NOUN'): {55, 83, 89},
     ('give', 'VERB'): {59},
     ('correspond', 'VERB'): {65},
     ('construct', 'VERB'): {68},
     ('support', 'VERB'): {71},
     ('use', 'VERB'): {77},
     ('solve', 'VERB'): {79},
     ('mixed', 'ADJ'): {88}}



Let's visualize the lemma graph, and for that first we need to collect a dictionary of the labels.


```python
labels = {}
keys = list(seen_lemma.keys())

for i in range(len(seen_lemma)):
    labels[i] = keys[i][0].lower()

labels
```




    {0: 'compatibility',
     1: 'system',
     2: 'linear',
     3: 'constraint',
     4: 'set',
     5: 'natural',
     6: 'number',
     7: 'criterion',
     8: 'diophantine',
     9: 'equation',
     10: 'strict',
     11: 'inequation',
     12: 'nonstrict',
     13: 'consider',
     14: 'upper',
     15: 'bound',
     16: 'component',
     17: 'minimal',
     18: 'solution',
     19: 'algorithm',
     20: 'construction',
     21: 'generating',
     22: 'type',
     23: 'give',
     24: 'correspond',
     25: 'construct',
     26: 'support',
     27: 'use',
     28: 'solve',
     29: 'mixed'}



Then use `matplotlib` to visualize the lemma graph:


```python
%matplotlib inline
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(9, 9))
pos = nx.spring_layout(lemma_graph)

nx.draw(lemma_graph, pos=pos, with_labels=False, font_weight="bold")
nx.draw_networkx_labels(lemma_graph, pos, labels);
```


    
![png](explain_algo_files/explain_algo_23_0.png)
    


Now to run the algorithm, we use `PageRank` – a form of
[*eigenvector centrality*](https://derwen.ai/docs/ptr/glossary/#eigenvector-centrality)
– to calculate ranks for each of the nodes in the lemma graph.


```python
ranks = nx.pagerank(lemma_graph)
ranks
```




    {0: 0.025190055141357165,
     1: 0.09709174565608479,
     2: 0.03658656272138432,
     3: 0.022947339381092696,
     4: 0.07548767636963792,
     5: 0.01884004785394172,
     6: 0.01884004785394172,
     7: 0.019767433918161055,
     8: 0.03093250736456608,
     9: 0.031636552282656216,
     10: 0.0250439175297852,
     11: 0.03969617593153302,
     12: 0.02513276636673567,
     13: 0.0390375393827704,
     14: 0.02428614673389346,
     15: 0.02428614673389346,
     16: 0.031629446298645975,
     17: 0.06334806476862227,
     18: 0.061826419749828485,
     19: 0.03201021345587308,
     20: 0.02404712231242087,
     21: 0.029468555366439973,
     22: 0.04816979699201436,
     23: 0.010894627731045426,
     24: 0.026930354700088012,
     25: 0.03165915652710971,
     26: 0.029382686223731833,
     27: 0.019263849959229938,
     28: 0.01982332786706688,
     29: 0.016743716826448173}




```python
for node_id, rank in sorted(ranks.items(), key=lambda x: x[1], reverse=True):
    ic(node_id, rank, labels[node_id])
```

    ic| node_id: 1, rank: 0.09709174565608479, labels[node_id]: 'system'
    ic| node_id: 4, rank: 0.07548767636963792, labels[node_id]: 'set'
    ic| node_id: 17, rank: 0.06334806476862227, labels[node_id]: 'minimal'
    ic| node_id: 18
        rank: 0.061826419749828485
        labels[node_id]: 'solution'
    ic| node_id: 22, rank: 0.04816979699201436, labels[node_id]: 'type'
    ic| node_id: 11
        rank: 0.03969617593153302
        labels[node_id]: 'inequation'
    ic| node_id: 13, rank: 0.0390375393827704, labels[node_id]: 'consider'
    ic| node_id: 2, rank: 0.03658656272138432, labels[node_id]: 'linear'
    ic| node_id: 19
        rank: 0.03201021345587308
        labels[node_id]: 'algorithm'
    ic| node_id: 25
        rank: 0.03165915652710971
        labels[node_id]: 'construct'
    ic| node_id: 9
        rank: 0.031636552282656216
        labels[node_id]: 'equation'
    ic| node_id: 16
        rank: 0.031629446298645975
        labels[node_id]: 'component'
    ic| node_id: 8
        rank: 0.03093250736456608
        labels[node_id]: 'diophantine'
    ic| node_id: 21
        rank: 0.029468555366439973
        labels[node_id]: 'generating'
    ic| node_id: 26
        rank: 0.029382686223731833
        labels[node_id]: 'support'
    ic| node_id: 24
        rank: 0.026930354700088012
        labels[node_id]: 'correspond'
    ic| node_id: 0
        rank: 0.025190055141357165
        labels[node_id]: 'compatibility'
    ic| node_id: 12
        rank: 0.02513276636673567
        labels[node_id]: 'nonstrict'
    ic| node_id: 10, rank: 0.0250439175297852, labels[node_id]: 'strict'
    ic| node_id: 14, rank: 0.02428614673389346, labels[node_id]: 'upper'
    ic| node_id: 15, rank: 0.02428614673389346, labels[node_id]: 'bound'
    ic| node_id: 20
        rank: 0.02404712231242087
        labels[node_id]: 'construction'
    ic| node_id: 3
        rank: 0.022947339381092696
        labels[node_id]: 'constraint'
    ic| node_id: 28, rank: 0.01982332786706688, labels[node_id]: 'solve'
    ic| node_id: 7
        rank: 0.019767433918161055
        labels[node_id]: 'criterion'
    ic| node_id: 27, rank: 0.019263849959229938, labels[node_id]: 'use'
    ic| node_id: 5, rank: 0.01884004785394172, labels[node_id]: 'natural'
    ic| node_id: 6, rank: 0.01884004785394172, labels[node_id]: 'number'
    ic| node_id: 29, rank: 0.016743716826448173, labels[node_id]: 'mixed'
    ic| node_id: 23, rank: 0.010894627731045426, labels[node_id]: 'give'


Define a function to collect the top-ranked phrases from the lemma graph.


```python
import math

def collect_phrases (chunk, phrases, counts):
    chunk_len = chunk.end - chunk.start
    sq_sum_rank = 0.0
    non_lemma = 0
    compound_key = set([])

    for i in range(chunk.start, chunk.end):
        token = doc[i]
        key = (token.lemma_, token.pos_)
        
        if key in seen_lemma:
            node_id = list(seen_lemma.keys()).index(key)
            rank = ranks[node_id]
            sq_sum_rank += rank
            compound_key.add(key)
        
            ic(token.lemma_, token.pos_, node_id, rank)
        else:
            non_lemma += 1
    
    # although the noun chunking is greedy, we discount the ranks using a
    # point estimate based on the number of non-lemma tokens within a phrase
    non_lemma_discount = chunk_len / (chunk_len + (2.0 * non_lemma) + 1.0)

    # use root mean square (RMS) to normalize the contributions of all the tokens
    phrase_rank = math.sqrt(sq_sum_rank / (chunk_len + non_lemma))
    phrase_rank *= non_lemma_discount

    # remove spurious punctuation
    phrase = chunk.text.lower().replace("'", "")

    # create a unique key for the the phrase based on its lemma components
    compound_key = tuple(sorted(list(compound_key)))
    
    if not compound_key in phrases:
        phrases[compound_key] = set([ (phrase, phrase_rank) ])
        counts[compound_key] = 1
    else:
        phrases[compound_key].add( (phrase, phrase_rank) )
        counts[compound_key] += 1

    ic(phrase_rank, chunk.text, chunk.start, chunk.end, chunk_len, counts[compound_key])
```

Collect the top-ranked phrases based on both the noun chunks and the named entities...


```python
phrases = {}
counts = {}

for chunk in doc.noun_chunks:
    collect_phrases(chunk, phrases, counts)
```

    ic| token.lemma_: 'compatibility'
        token.pos_: 'NOUN'
        node_id: 0
        rank: 0.025190055141357165
    ic| phrase_rank: 0.07935687610622845
        chunk.text: 'Compatibility'
        chunk.start: 0
        chunk.end: 1
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'system'
        token.pos_: 'NOUN'
        node_id: 1
        rank: 0.09709174565608479
    ic| phrase_rank: 0.15579774200552843
        chunk.text: 'systems'
        chunk.start: 2
        chunk.end: 3
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'linear'
        token.pos_: 'ADJ'
        node_id: 2
        rank: 0.03658656272138432
    ic| token.lemma_: 'constraint'
        token.pos_: 'NOUN'
        node_id: 3
        rank: 0.022947339381092696
    ic| phrase_rank: 0.11502067650110856
        chunk.text: 'linear constraints'
        chunk.start: 4
        chunk.end: 6
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'set'
        token.pos_: 'NOUN'
        node_id: 4
        rank: 0.07548767636963792
    ic| phrase_rank: 0.06345084244027568
        chunk.text: 'the set'
        chunk.start: 7
        chunk.end: 9
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'natural'
        token.pos_: 'ADJ'
        node_id: 5
        rank: 0.01884004785394172
    ic| token.lemma_: 'number'
        token.pos_: 'NOUN'
        node_id: 6
        rank: 0.01884004785394172
    ic| phrase_rank: 0.09150603587606598
        chunk.text: 'natural numbers'
        chunk.start: 10
        chunk.end: 12
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'criterion'
        token.pos_: 'NOUN'
        node_id: 7
        rank: 0.019767433918161055
    ic| phrase_rank: 0.07029835332026109
        chunk.text: 'Criteria'
        chunk.start: 13
        chunk.end: 14
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'compatibility'
        token.pos_: 'NOUN'
        node_id: 0
        rank: 0.025190055141357165
    ic| phrase_rank: 0.07935687610622845
        chunk.text: 'compatibility'
        chunk.start: 15
        chunk.end: 16
        chunk_len: 1
        counts[compound_key]: 2
    ic| token.lemma_: 'system'
        token.pos_: 'NOUN'
        node_id: 1
        rank: 0.09709174565608479
    ic| phrase_rank: 0.07195989462882217
        chunk.text: 'a system'
        chunk.start: 17
        chunk.end: 19
        chunk_len: 2
        counts[compound_key]: 2
    ic| token.lemma_: 'linear'
        token.pos_: 'ADJ'
        node_id: 2
        rank: 0.03658656272138432
    ic| token.lemma_: 'Diophantine'
        token.pos_: 'PROPN'
        node_id: 8
        rank: 0.03093250736456608
    ic| token.lemma_: 'equation'
        token.pos_: 'NOUN'
        node_id: 9
        rank: 0.031636552282656216
    ic| phrase_rank: 0.13635130800294415
        chunk.text: 'linear Diophantine equations'
        chunk.start: 20
        chunk.end: 23
        chunk_len: 3
        counts[compound_key]: 1
    ic| token.lemma_: 'strict'
        token.pos_: 'ADJ'
        node_id: 10
        rank: 0.0250439175297852
    ic| token.lemma_: 'inequation'
        token.pos_: 'NOUN'
        node_id: 11
        rank: 0.03969617593153302
    ic| phrase_rank: 0.11994451815672316
        chunk.text: 'strict inequations'
        chunk.start: 24
        chunk.end: 26
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'nonstrict'
        token.pos_: 'ADJ'
        node_id: 12
        rank: 0.02513276636673567
    ic| token.lemma_: 'inequation'
        token.pos_: 'NOUN'
        node_id: 11
        rank: 0.03969617593153302
    ic| phrase_rank: 0.12002679543267614
        chunk.text: 'nonstrict inequations'
        chunk.start: 28
        chunk.end: 30
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'Upper'
        token.pos_: 'PROPN'
        node_id: 14
        rank: 0.02428614673389346
    ic| token.lemma_: 'bound'
        token.pos_: 'NOUN'
        node_id: 15
        rank: 0.02428614673389346
    ic| phrase_rank: 0.10389342131646997
        chunk.text: 'Upper bounds'
        chunk.start: 33
        chunk.end: 35
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'component'
        token.pos_: 'NOUN'
        node_id: 16
        rank: 0.031629446298645975
    ic| phrase_rank: 0.08892334662315343
        chunk.text: 'components'
        chunk.start: 36
        chunk.end: 37
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'minimal'
        token.pos_: 'ADJ'
        node_id: 17
        rank: 0.06334806476862227
    ic| token.lemma_: 'set'
        token.pos_: 'NOUN'
        node_id: 4
        rank: 0.07548767636963792
    ic| phrase_rank: 0.09315167105930662
        chunk.text: 'a minimal set'
        chunk.start: 38
        chunk.end: 41
        chunk_len: 3
        counts[compound_key]: 1
    ic| token.lemma_: 'solution'
        token.pos_: 'NOUN'
        node_id: 18
        rank: 0.061826419749828485
    ic| phrase_rank: 0.12432459506251015
        chunk.text: 'solutions'
        chunk.start: 42
        chunk.end: 43
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'algorithm'
        token.pos_: 'NOUN'
        node_id: 19
        rank: 0.03201021345587308
    ic| phrase_rank: 0.08945699169974514
        chunk.text: 'algorithms'
        chunk.start: 44
        chunk.end: 45
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'construction'
        token.pos_: 'NOUN'
        node_id: 20
        rank: 0.02404712231242087
    ic| phrase_rank: 0.07753567293901058
        chunk.text: 'construction'
        chunk.start: 46
        chunk.end: 47
        chunk_len: 1
        counts[compound_key]: 1
    ic| token.lemma_: 'minimal'
        token.pos_: 'ADJ'
        node_id: 17
        rank: 0.06334806476862227
    ic| token.lemma_: 'generating'
        token.pos_: 'NOUN'
        node_id: 21
        rank: 0.029468555366439973
    ic| token.lemma_: 'set'
        token.pos_: 'NOUN'
        node_id: 4
        rank: 0.07548767636963792
    ic| phrase_rank: 0.17764305670256655
        chunk.text: 'minimal generating sets'
        chunk.start: 48
        chunk.end: 51
        chunk_len: 3
        counts[compound_key]: 1
    ic| token.lemma_: 'solution'
        token.pos_: 'NOUN'
        node_id: 18
        rank: 0.061826419749828485
    ic| phrase_rank: 0.12432459506251015
        chunk.text: 'solutions'
        chunk.start: 52
        chunk.end: 53
        chunk_len: 1
        counts[compound_key]: 2
    ic| token.lemma_: 'type'
        token.pos_: 'NOUN'
        node_id: 22
        rank: 0.04816979699201436
    ic| phrase_rank: 0.050685854432712285
        chunk.text: 'all types'
        chunk.start: 54
        chunk.end: 56
        chunk_len: 2
        counts[compound_key]: 1
    ic| token.lemma_: 'system'
        token.pos_: 'NOUN'
        node_id: 1
        rank: 0.09709174565608479
    ic| phrase_rank: 0.15579774200552843
        chunk.text: 'systems'
        chunk.start: 57
        chunk.end: 58
        chunk_len: 1
        counts[compound_key]: 3
    ic| token.lemma_: 'criterion'
        token.pos_: 'NOUN'
        node_id: 7
        rank: 0.019767433918161055
    ic| phrase_rank: 0.03246941857043213
        chunk.text: 'These criteria'
        chunk.start: 61
        chunk.end: 63
        chunk_len: 2
        counts[compound_key]: 2
    ic| token.lemma_: 'correspond'
        token.pos_: 'VERB'
        node_id: 24
        rank: 0.026930354700088012
    ic| token.lemma_: 'algorithm'
        token.pos_: 'NOUN'
        node_id: 19
        rank: 0.03201021345587308
    ic| phrase_rank: 0.0606941966727262
        chunk.text: 'the corresponding algorithms'
        chunk.start: 64
        chunk.end: 67
        chunk_len: 3
        counts[compound_key]: 1
    ic| token.lemma_: 'minimal'
        token.pos_: 'ADJ'
        node_id: 17
        rank: 0.06334806476862227
    ic| token.lemma_: 'support'
        token.pos_: 'VERB'
        node_id: 26
        rank: 0.029382686223731833
    ic| token.lemma_: 'set'
        token.pos_: 'NOUN'
        node_id: 4
        rank: 0.07548767636963792
    ic| phrase_rank: 0.10481265770639074
        chunk.text: 'a minimal supporting set'
        chunk.start: 69
        chunk.end: 73
        chunk_len: 4
        counts[compound_key]: 1
    ic| token.lemma_: 'solution'
        token.pos_: 'NOUN'
        node_id: 18
        rank: 0.061826419749828485
    ic| phrase_rank: 0.12432459506251015
        chunk.text: 'solutions'
        chunk.start: 74
        chunk.end: 75
        chunk_len: 1
        counts[compound_key]: 3
    ic| token.lemma_: 'consider'
        token.pos_: 'VERB'
        node_id: 13
        rank: 0.0390375393827704
    ic| token.lemma_: 'type'
        token.pos_: 'NOUN'
        node_id: 22
        rank: 0.04816979699201436
    ic| token.lemma_: 'system'
        token.pos_: 'NOUN'
        node_id: 1
        rank: 0.09709174565608479
    ic| phrase_rank: 0.0811302044403381
        chunk.text: 'all the considered types systems'
        chunk.start: 80
        chunk.end: 85
        chunk_len: 5
        counts[compound_key]: 1
    ic| token.lemma_: 'system'
        token.pos_: 'NOUN'
        node_id: 1
        rank: 0.09709174565608479
    ic| phrase_rank: 0.15579774200552843
        chunk.text: 'systems'
        chunk.start: 86
        chunk.end: 87
        chunk_len: 1
        counts[compound_key]: 4
    ic| token.lemma_: 'mixed'
        token.pos_: 'ADJ'
        node_id: 29
        rank: 0.016743716826448173
    ic| token.lemma_: 'type'
        token.pos_: 'NOUN'
        node_id: 22
        rank: 0.04816979699201436
    ic| phrase_rank: 0.12010505939797736
        chunk.text: 'mixed types'
        chunk.start: 88
        chunk.end: 90
        chunk_len: 2
        counts[compound_key]: 1



```python
for ent in doc.ents:
    collect_phrases(ent, phrases, counts)
```

    ic| token.lemma_: 'Diophantine'
        token.pos_: 'PROPN'
        node_id: 8
        rank: 0.03093250736456608
    ic| phrase_rank: 0.08793819898736567
        chunk.text: 'Diophantine'
        chunk.start: 21
        chunk.end: 22
        chunk_len: 1
        counts[compound_key]: 1


Since noun chunks can be expressed in different ways (e.g., they may have articles or prepositions), we need to find a minimum span for each phrase based on combinations of lemmas...


```python
import operator

min_phrases = {}

for compound_key, rank_tuples in phrases.items():
    l = list(rank_tuples)
    l.sort(key=operator.itemgetter(1), reverse=True)
    
    phrase, rank = l[0]
    count = counts[compound_key]
    
    min_phrases[phrase] = (rank, count)
```

Then let's examine the results of TextRank...


```python
for phrase, (rank, count) in sorted(min_phrases.items(), key=lambda x: x[1][0], reverse=True):
    ic(phrase, count, rank)
```

    ic| phrase: 'minimal generating sets'
        count: 1
        rank: 0.17764305670256655
    ic| phrase: 'systems', count: 4, rank: 0.15579774200552843
    ic| phrase: 'linear diophantine equations'
        count: 1
        rank: 0.13635130800294415
    ic| phrase: 'solutions', count: 3, rank: 0.12432459506251015
    ic| phrase: 'mixed types', count: 1, rank: 0.12010505939797736
    ic| phrase: 'nonstrict inequations'
        count: 1
        rank: 0.12002679543267614
    ic| phrase: 'strict inequations', count: 1, rank: 0.11994451815672316
    ic| phrase: 'linear constraints', count: 1, rank: 0.11502067650110856
    ic| phrase: 'a minimal supporting set'
        count: 1
        rank: 0.10481265770639074
    ic| phrase: 'upper bounds', count: 1, rank: 0.10389342131646997
    ic| phrase: 'a minimal set', count: 1, rank: 0.09315167105930662
    ic| phrase: 'natural numbers', count: 1, rank: 0.09150603587606598
    ic| phrase: 'algorithms', count: 1, rank: 0.08945699169974514
    ic| phrase: 'components', count: 1, rank: 0.08892334662315343
    ic| phrase: 'diophantine', count: 1, rank: 0.08793819898736567
    ic| phrase: 'all the considered types systems'
        count: 1
        rank: 0.0811302044403381
    ic| phrase: 'compatibility', count: 2, rank: 0.07935687610622845
    ic| phrase: 'construction', count: 1, rank: 0.07753567293901058
    ic| phrase: 'criteria', count: 2, rank: 0.07029835332026109
    ic| phrase: 'the set', count: 1, rank: 0.06345084244027568
    ic| phrase: 'the corresponding algorithms'
        count: 1
        rank: 0.0606941966727262
    ic| phrase: 'all types', count: 1, rank: 0.050685854432712285


Just for kicks, compare with raw results of the non-chunked lemma nodes...


```python
for node_id, rank in sorted(ranks.items(), key=lambda x: x[1], reverse=True):
    ic(labels[node_id], rank)
```

    ic| labels[node_id]: 'system', rank: 0.09709174565608479
    ic| labels[node_id]: 'set', rank: 0.07548767636963792
    ic| labels[node_id]: 'minimal', rank: 0.06334806476862227
    ic| labels[node_id]: 'solution', rank: 0.061826419749828485
    ic| labels[node_id]: 'type', rank: 0.04816979699201436
    ic| labels[node_id]: 'inequation', rank: 0.03969617593153302
    ic| labels[node_id]: 'consider', rank: 0.0390375393827704
    ic| labels[node_id]: 'linear', rank: 0.03658656272138432
    ic| labels[node_id]: 'algorithm', rank: 0.03201021345587308
    ic| labels[node_id]: 'construct', rank: 0.03165915652710971
    ic| labels[node_id]: 'equation', rank: 0.031636552282656216
    ic| labels[node_id]: 'component', rank: 0.031629446298645975
    ic| labels[node_id]: 'diophantine', rank: 0.03093250736456608
    ic| labels[node_id]: 'generating', rank: 0.029468555366439973
    ic| labels[node_id]: 'support', rank: 0.029382686223731833
    ic| labels[node_id]: 'correspond', rank: 0.026930354700088012
    ic| labels[node_id]: 'compatibility', rank: 0.025190055141357165
    ic| labels[node_id]: 'nonstrict', rank: 0.02513276636673567
    ic| labels[node_id]: 'strict', rank: 0.0250439175297852
    ic| labels[node_id]: 'upper', rank: 0.02428614673389346
    ic| labels[node_id]: 'bound', rank: 0.02428614673389346
    ic| labels[node_id]: 'construction', rank: 0.02404712231242087
    ic| labels[node_id]: 'constraint', rank: 0.022947339381092696
    ic| labels[node_id]: 'solve', rank: 0.01982332786706688
    ic| labels[node_id]: 'criterion', rank: 0.019767433918161055
    ic| labels[node_id]: 'use', rank: 0.019263849959229938
    ic| labels[node_id]: 'natural', rank: 0.01884004785394172
    ic| labels[node_id]: 'number', rank: 0.01884004785394172
    ic| labels[node_id]: 'mixed', rank: 0.016743716826448173
    ic| labels[node_id]: 'give', rank: 0.010894627731045426

