

!!! note
    To run this notebook in JupyterLab, load [`examples/explain_summ.ipynb`](https://github.com/DerwenAI/pytextrank/blob/main/examples/explain_summ.ipynb)



# Explain PyTextRank: extractive summarization

How does **PyTextRank** perform *extractive summarization* on a text document?

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

Create some text to use....


```python
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."
```

Then add **PyTextRank** into the `spaCy` pipeline...


```python
import pytextrank

nlp.add_pipe("textrank", last=True)
doc = nlp(text)
```

Examine the results: a list of top-ranked phrases in the document


```python
from icecream import ic

for p in doc._.phrases:
    ic(p.rank, p.count, p.text)
    ic(p.chunks)
```

    ic| p.rank: 0.18359439311764025, p.count: 1, p.text: 'mixed types'
    ic| p.chunks: [mixed types]
    ic| p.rank: 0.17847961931078207, p.count: 3, p.text: 'systems'
    ic| p.chunks: [systems, systems, systems]
    ic| p.rank: 0.15037838042245094
        p.count: 1
        p.text: 'minimal generating sets'
    ic| p.chunks: [minimal generating sets]
    ic| p.rank: 0.14740065982407316
        p.count: 1
        p.text: 'nonstrict inequations'
    ic| p.chunks: [nonstrict inequations]
    ic| p.rank: 0.13946027725597837
        p.count: 1
        p.text: 'strict inequations'
    ic| p.chunks: [strict inequations]
    ic| p.rank: 0.1195023546245721
        p.count: 1
        p.text: 'linear Diophantine equations'
    ic| p.chunks: [linear Diophantine equations]
    ic| p.rank: 0.11450088293222845, p.count: 1, p.text: 'natural numbers'
    ic| p.chunks: [natural numbers]
    ic| p.rank: 0.1078071817368632, p.count: 3, p.text: 'solutions'
    ic| p.chunks: [solutions, solutions, solutions]
    ic| p.rank: 0.10529828014583348
        p.count: 1
        p.text: 'linear constraints'
    ic| p.chunks: [linear constraints]
    ic| p.rank: 0.10369605907081418
        p.count: 1
        p.text: 'all the considered types systems'
    ic| p.chunks: [all the considered types systems]
    ic| p.rank: 0.08812713074893187
        p.count: 1
        p.text: 'a minimal supporting set'
    ic| p.chunks: [a minimal supporting set]
    ic| p.rank: 0.08243620500315357, p.count: 1, p.text: 'a system'
    ic| p.chunks: [a system]
    ic| p.rank: 0.07944607954086784, p.count: 1, p.text: 'a minimal set'
    ic| p.chunks: [a minimal set]
    ic| p.rank: 0.0763527926213032, p.count: 1, p.text: 'algorithms'
    ic| p.chunks: [algorithms]
    ic| p.rank: 0.07593126037016427, p.count: 1, p.text: 'all types'
    ic| p.chunks: [all types]
    ic| p.rank: 0.07309361902551356, p.count: 1, p.text: 'Diophantine'
    ic| p.chunks: [Diophantine]
    ic| p.rank: 0.0702090100898443, p.count: 1, p.text: 'construction'
    ic| p.chunks: [construction]
    ic| p.rank: 0.060225391238828516, p.count: 1, p.text: 'Upper bounds'
    ic| p.chunks: [Upper bounds]
    ic| p.rank: 0.05800111772673988, p.count: 1, p.text: 'the set'
    ic| p.chunks: [the set]
    ic| p.rank: 0.05425139476531647, p.count: 1, p.text: 'components'
    ic| p.chunks: [components]
    ic| p.rank: 0.04516904342912139, p.count: 1, p.text: 'Compatibility'
    ic| p.chunks: [Compatibility]
    ic| p.rank: 0.04516904342912139, p.count: 1, p.text: 'compatibility'
    ic| p.chunks: [compatibility]
    ic| p.rank: 0.04435648606848154
        p.count: 1
        p.text: 'the corresponding algorithms'
    ic| p.chunks: [the corresponding algorithms]
    ic| p.rank: 0.042273783712246285, p.count: 1, p.text: 'Criteria'
    ic| p.chunks: [Criteria]
    ic| p.rank: 0.01952542432474353, p.count: 1, p.text: 'These criteria'
    ic| p.chunks: [These criteria]


Construct a list of the sentence boundaries with a phrase vector (initialized to empty set) for each...


```python
sent_bounds = [ [s.start, s.end, set([])] for s in doc.sents ]
sent_bounds
```




    [[0, 13, set()], [13, 33, set()], [33, 61, set()], [61, 91, set()]]



Iterate through the top-ranked phrases, added them to the phrase vector for each sentence...


```python
limit_phrases = 4

phrase_id = 0
unit_vector = []

for p in doc._.phrases:
    ic(phrase_id, p.text, p.rank)
    
    unit_vector.append(p.rank)
    
    for chunk in p.chunks:
        ic(chunk.start, chunk.end)
        
        for sent_start, sent_end, sent_vector in sent_bounds:
            if chunk.start >= sent_start and chunk.end <= sent_end:
                ic(sent_start, chunk.start, chunk.end, sent_end)
                sent_vector.add(phrase_id)
                break

    phrase_id += 1

    if phrase_id == limit_phrases:
        break
```

    ic| phrase_id: 0, p.text: 'mixed types', p.rank: 0.18359439311764025
    ic| chunk.start: 88, chunk.end: 90
    ic| sent_start: 61, chunk.start: 88, chunk.end: 90, sent_end: 91
    ic| phrase_id: 1, p.text: 'systems', p.rank: 0.17847961931078207
    ic| chunk.start: 2, chunk.end: 3
    ic| sent_start: 0, chunk.start: 2, chunk.end: 3, sent_end: 13
    ic| chunk.start: 57, chunk.end: 58
    ic| sent_start: 33, chunk.start: 57, chunk.end: 58, sent_end: 61
    ic| chunk.start: 86, chunk.end: 87
    ic| sent_start: 61, chunk.start: 86, chunk.end: 87, sent_end: 91
    ic| phrase_id: 2
        p.text: 'minimal generating sets'
        p.rank: 0.15037838042245094
    ic| chunk.start: 48, chunk.end: 51
    ic| sent_start: 33, chunk.start: 48, chunk.end: 51, sent_end: 61
    ic| phrase_id: 3
        p.text: 'nonstrict inequations'
        p.rank: 0.14740065982407316
    ic| chunk.start: 28, chunk.end: 30
    ic| sent_start: 13, chunk.start: 28, chunk.end: 30, sent_end: 33


Let's take a look at the results...


```python
sent_bounds
```




    [[0, 13, {1}], [13, 33, {3}], [33, 61, {1, 2}], [61, 91, {0, 1}]]




```python
for sent in doc.sents:
    ic(sent)
```

    ic| sent: Compatibility of systems of linear constraints over the set of natural numbers.
    ic| sent: Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered.
    ic| sent: Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given.
    ic| sent: These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.


We also construct a `unit_vector` for all of the phrases, up to the limit requested...


```python
unit_vector
```




    [0.18359439311764025,
     0.17847961931078207,
     0.15037838042245094,
     0.14740065982407316]



Then normalized...


```python
sum_ranks = sum(unit_vector)

unit_vector = [ rank/sum_ranks for rank in unit_vector ]
unit_vector
```




    [0.2782352712825618,
     0.2704838881736656,
     0.2278967715809441,
     0.22338406896282853]



Iterate through each sentence, calculating its *euclidean distance* from the unit vector...


```python
from math import sqrt

sent_rank = {}
sent_id = 0

for sent_start, sent_end, sent_vector in sent_bounds:
    ic(sent_vector)
    sum_sq = 0.0
    ic
    for phrase_id in range(len(unit_vector)):
        ic(phrase_id, unit_vector[phrase_id])
        
        if phrase_id not in sent_vector:
            sum_sq += unit_vector[phrase_id]**2.0

    sent_rank[sent_id] = sqrt(sum_sq)
    sent_id += 1
```

    ic| sent_vector: {1}
    ic| phrase_id: 0, unit_vector[phrase_id]: 0.2782352712825618
    ic| phrase_id: 1, unit_vector[phrase_id]: 0.2704838881736656
    ic| phrase_id: 2, unit_vector[phrase_id]: 0.2278967715809441
    ic| phrase_id: 3, unit_vector[phrase_id]: 0.22338406896282853
    ic| sent_vector: {3}
    ic| phrase_id: 0, unit_vector[phrase_id]: 0.2782352712825618
    ic| phrase_id: 1, unit_vector[phrase_id]: 0.2704838881736656
    ic| phrase_id: 2, unit_vector[phrase_id]: 0.2278967715809441
    ic| phrase_id: 3, unit_vector[phrase_id]: 0.22338406896282853
    ic| sent_vector: {1, 2}
    ic| phrase_id: 0, unit_vector[phrase_id]: 0.2782352712825618
    ic| phrase_id: 1, unit_vector[phrase_id]: 0.2704838881736656
    ic| phrase_id: 2, unit_vector[phrase_id]: 0.2278967715809441
    ic| phrase_id: 3, unit_vector[phrase_id]: 0.22338406896282853
    ic| sent_vector: {0, 1}
    ic| phrase_id: 0, unit_vector[phrase_id]: 0.2782352712825618
    ic| phrase_id: 1, unit_vector[phrase_id]: 0.2704838881736656
    ic| phrase_id: 2, unit_vector[phrase_id]: 0.2278967715809441
    ic| phrase_id: 3, unit_vector[phrase_id]: 0.22338406896282853



```python
ic(sent_rank)
```

    ic| sent_rank: {0: 0.4233819161809908,
                    1: 0.4500148202495578,
                    2: 0.3568127078063091,
                    3: 0.31911969660835215}





    {0: 0.4233819161809908,
     1: 0.4500148202495578,
     2: 0.3568127078063091,
     3: 0.31911969660835215}



Sort the sentence indexes in descending order


```python
from operator import itemgetter

sorted(sent_rank.items(), key=itemgetter(1)) 
```




    [(3, 0.31911969660835215),
     (2, 0.3568127078063091),
     (0, 0.4233819161809908),
     (1, 0.4500148202495578)]



Extract the sentences with the lowest distance, up to the limit requested...


```python
limit_sentences = 2

sent_text = {}
sent_id = 0

for sent in doc.sents:
    sent_text[sent_id] = sent.text
    sent_id += 1

num_sent = 0

for sent_id, rank in sorted(sent_rank.items(), key=itemgetter(1)):
    ic(sent_id, sent_text[sent_id])
    num_sent += 1
    
    if num_sent == limit_sentences:
        break
```

    ic| sent_id: 3
        sent_text[sent_id]: ('These criteria and the corresponding algorithms for constructing a minimal '
                             'supporting set of solutions can be used in solving all the considered types '
                             'systems and systems of mixed types.')
    ic| sent_id: 2
        sent_text[sent_id]: ('Upper bounds for components of a minimal set of solutions and algorithms of '
                             'construction of minimal generating sets of solutions for all types of '
                             'systems are given.')

