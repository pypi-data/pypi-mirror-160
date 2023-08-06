

!!! note
    To run this notebook in JupyterLab, load [`examples/sample.ipynb`](https://github.com/DerwenAI/pytextrank/blob/main/examples/sample.ipynb)



# Getting Started

First, we'll import the required libraries and add the **PyTextRank** component into the `spaCy` pipeline:


```python
import pytextrank
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank");
```

Let's take a look at this pipeline now...


```python
nlp.pipe_names
```




    ['tok2vec',
     'tagger',
     'parser',
     'attribute_ruler',
     'lemmatizer',
     'ner',
     'textrank']



We can examine the `spaCy` pipeline in much greater detail...


```python
nlp.analyze_pipes(pretty=True)
```

    [1m
    ============================= Pipeline Overview =============================[0m
    
    #   Component         Assigns               Requires   Scores             Retokenizes
    -   ---------------   -------------------   --------   ----------------   -----------
    0   tok2vec           doc.tensor                                          False      
                                                                                         
    1   tagger            token.tag                        tag_acc            False      
                                                                                         
    2   parser            token.dep                        dep_uas            False      
                          token.head                       dep_las                       
                          token.is_sent_start              dep_las_per_type              
                          doc.sents                        sents_p                       
                                                           sents_r                       
                                                           sents_f                       
                                                                                         
    3   attribute_ruler                                                       False      
                                                                                         
    4   lemmatizer        token.lemma                      lemma_acc          False      
                                                                                         
    5   ner               doc.ents                         ents_f             False      
                          token.ent_iob                    ents_p                        
                          token.ent_type                   ents_r                        
                                                           ents_per_type                 
                                                                                         
    6   textrank                                                              False      
    
    [38;5;2m✔ No problems found.[0m





    {'summary': {'tok2vec': {'assigns': ['doc.tensor'],
       'requires': [],
       'scores': [],
       'retokenizes': False},
      'tagger': {'assigns': ['token.tag'],
       'requires': [],
       'scores': ['tag_acc'],
       'retokenizes': False},
      'parser': {'assigns': ['token.dep',
        'token.head',
        'token.is_sent_start',
        'doc.sents'],
       'requires': [],
       'scores': ['dep_uas',
        'dep_las',
        'dep_las_per_type',
        'sents_p',
        'sents_r',
        'sents_f'],
       'retokenizes': False},
      'attribute_ruler': {'assigns': [],
       'requires': [],
       'scores': [],
       'retokenizes': False},
      'lemmatizer': {'assigns': ['token.lemma'],
       'requires': [],
       'scores': ['lemma_acc'],
       'retokenizes': False},
      'ner': {'assigns': ['doc.ents', 'token.ent_iob', 'token.ent_type'],
       'requires': [],
       'scores': ['ents_f', 'ents_p', 'ents_r', 'ents_per_type'],
       'retokenizes': False},
      'textrank': {'assigns': [],
       'requires': [],
       'scores': [],
       'retokenizes': False}},
     'problems': {'tok2vec': [],
      'tagger': [],
      'parser': [],
      'attribute_ruler': [],
      'lemmatizer': [],
      'ner': [],
      'textrank': []},
     'attrs': {'token.ent_iob': {'assigns': ['ner'], 'requires': []},
      'token.ent_type': {'assigns': ['ner'], 'requires': []},
      'token.tag': {'assigns': ['tagger'], 'requires': []},
      'token.dep': {'assigns': ['parser'], 'requires': []},
      'token.head': {'assigns': ['parser'], 'requires': []},
      'doc.sents': {'assigns': ['parser'], 'requires': []},
      'doc.ents': {'assigns': ['ner'], 'requires': []},
      'doc.tensor': {'assigns': ['tok2vec'], 'requires': []},
      'token.lemma': {'assigns': ['lemmatizer'], 'requires': []},
      'token.is_sent_start': {'assigns': ['parser'], 'requires': []}}}



Next, let's load some text from a document:


```python
from icecream import ic
import pathlib

text = pathlib.Path("../dat/mih.txt").read_text()
text
```




    'Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types.\n'



Then run the `spaCy` pipeline...


```python
doc = nlp(text)
len(doc)
```




    92



Now we can access the **PyTextRank** component within the `spaCy` pipeline, and use it to get more information for post-processing of the document.
For example, let's see what the elapsed time in milliseconds was for the *TextRank* processing:


```python
tr = doc._.textrank
ic(tr.elapsed_time);
```

    ic| tr.elapsed_time: 5.707979202270508


Let's examine the top-ranked phrases in the document


```python
for phrase in doc._.phrases:
    ic(phrase.rank, phrase.count, phrase.text)
    ic(phrase.chunks)
```

    ic| phrase.rank: 0.17054248030845812
        phrase.count: 1
        phrase.text: 'mixed types'
    ic| phrase.chunks: [mixed types]
    ic| phrase.rank: 0.15757771579579002
        phrase.count: 1
        phrase.text: 'minimal generating sets'
    ic| phrase.chunks: [minimal generating sets]
    ic| phrase.rank: 0.1573942320091846
        phrase.count: 3
        phrase.text: 'systems'
    ic| phrase.chunks: [systems, systems, systems]
    ic| phrase.rank: 0.14894241299658317
        phrase.count: 1
        phrase.text: 'nonstrict inequations'
    ic| phrase.chunks: [nonstrict inequations]
    ic| phrase.rank: 0.14039169904589088
        phrase.count: 1
        phrase.text: 'strict inequations'
    ic| phrase.chunks: [strict inequations]
    ic| phrase.rank: 0.11698198658021898
        phrase.count: 1
        phrase.text: 'natural numbers'
    ic| phrase.chunks: [natural numbers]
    ic| phrase.rank: 0.11559770516796158
        phrase.count: 1
        phrase.text: 'linear Diophantine equations'
    ic| phrase.chunks: [linear Diophantine equations]
    ic| phrase.rank: 0.11407086615794945
        phrase.count: 3
        phrase.text: 'solutions'
    ic| phrase.chunks: [solutions, solutions, solutions]
    ic| phrase.rank: 0.10165710454752863
        phrase.count: 1
        phrase.text: 'linear constraints'
    ic| phrase.chunks: [linear constraints]
    ic| phrase.rank: 0.09237587396226833
        phrase.count: 1
        phrase.text: 'a minimal supporting set'
    ic| phrase.chunks: [a minimal supporting set]
    ic| phrase.rank: 0.08845296671843554
        phrase.count: 1
        phrase.text: 'all the considered types systems'
    ic| phrase.chunks: [all the considered types systems]
    ic| phrase.rank: 0.08294839224739124
        phrase.count: 1
        phrase.text: 'a minimal set'
    ic| phrase.chunks: [a minimal set]
    ic| phrase.rank: 0.08107274369298882
        phrase.count: 1
        phrase.text: 'algorithms'
    ic| phrase.chunks: [algorithms]
    ic| phrase.rank: 0.07429406639612553
        phrase.count: 1
        phrase.text: 'construction'
    ic| phrase.chunks: [construction]
    ic| phrase.rank: 0.07269728177551771
        phrase.count: 1
        phrase.text: 'a system'
    ic| phrase.chunks: [a system]
    ic| phrase.rank: 0.07130948853545689
        phrase.count: 1
        phrase.text: 'Diophantine'
    ic| phrase.chunks: [Diophantine]
    ic| phrase.rank: 0.07034880604533804
        phrase.count: 1
        phrase.text: 'all types'
    ic| phrase.chunks: [all types]
    ic| phrase.rank: 0.06480303503167001
        phrase.count: 1
        phrase.text: 'Upper bounds'
    ic| phrase.chunks: [Upper bounds]
    ic| phrase.rank: 0.05969087234318076
        phrase.count: 1
        phrase.text: 'the set'
    ic| phrase.chunks: [the set]
    ic| phrase.rank: 0.05837512270115124
        phrase.count: 1
        phrase.text: 'components'
    ic| phrase.chunks: [components]
    ic| phrase.rank: 0.048602276273752514
        phrase.count: 1
        phrase.text: 'Compatibility'
    ic| phrase.chunks: [Compatibility]
    ic| phrase.rank: 0.048602276273752514
        phrase.count: 1
        phrase.text: 'compatibility'
    ic| phrase.chunks: [compatibility]
    ic| phrase.rank: 0.0472624878442175
        phrase.count: 1
        phrase.text: 'the corresponding algorithms'
    ic| phrase.chunks: [the corresponding algorithms]
    ic| phrase.rank: 0.04548690742119631
        phrase.count: 1
        phrase.text: 'Criteria'
    ic| phrase.chunks: [Criteria]
    ic| phrase.rank: 0.021009502595385022
        phrase.count: 1
        phrase.text: 'These criteria'
    ic| phrase.chunks: [These criteria]


## Stop Words

To show use of the *stop words* feature, first we'll output a baseline...


```python
text = pathlib.Path("../dat/gen.txt").read_text()
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='words', chunks=[words, words], count=2, rank=0.15746606699141763)
    ic| phrase: Phrase(text='sentences', chunks=[sentences], count=1, rank=0.12965916420829138)
    ic| phrase: Phrase(text='Mihalcea et al', chunks=[Mihalcea et al], count=1, rank=0.10571655249620954)
    ic| phrase: Phrase(text='the remaining words', chunks=[the remaining words], count=1, rank=0.09329379463860477)
    ic| phrase: Phrase(text='gensim implements TextRank', chunks=[gensim implements TextRank], count=1, rank=0.08981955768260336)
    ic| phrase: Phrase(text='text summarization', chunks=[text summarization], count=1, rank=0.0843351188899575)
    ic| phrase: Phrase(text='ranking webpages', chunks=[ranking webpages], count=1, rank=0.07936404910104827)
    ic| phrase: Phrase(text='Okapi BM25 function', chunks=[Okapi BM25 function], count=1, rank=0.07400094270083186)
    ic| phrase: Phrase(text='every other sentence', chunks=[every other sentence], count=1, rank=0.07073416034725326)
    ic| phrase: Phrase(text='original TextRank', chunks=[original TextRank], count=1, rank=0.06710956557420322)


Notice how the top-ranked phrase above is `words` ?
Let's add that phrase to our *stop words* list, to exclude it from the ranked phrases...


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] } })

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='sentences', chunks=[sentences], count=1, rank=0.14407775200046075)
    ic| phrase: Phrase(text='Mihalcea et al', chunks=[Mihalcea et al], count=1, rank=0.11286475216345385)
    ic| phrase: Phrase(text='gensim implements TextRank', chunks=[gensim implements TextRank], count=1, rank=0.09589788430130489)
    ic| phrase: Phrase(text='text summarization', chunks=[text summarization], count=1, rank=0.09004754289053603)
    ic| phrase: Phrase(text='ranking webpages', chunks=[ranking webpages], count=1, rank=0.08473538778364878)
    ic| phrase: Phrase(text='every other sentence', chunks=[every other sentence], count=1, rank=0.07909136977858265)
    ic| phrase: Phrase(text='Okapi BM25 function', chunks=[Okapi BM25 function], count=1, rank=0.07900911166567022)
    ic| phrase: Phrase(text='original TextRank', chunks=[original TextRank], count=1, rank=0.07165073049436399)
    ic| phrase: Phrase(text='TextRank', chunks=[TextRank, TextRank, TextRank, TextRank], count=4, rank=0.06888311869751775)
    ic| phrase: Phrase(text='every sentence', chunks=[every sentence], count=1, rank=0.06654666312136172)


For each entry, you'll need to add a key that is the *lemma* and a value that's a list of its *part-of-speech* tags.

## Scrubber

Observe how different variations of "sentence", like "every sentence" and "every other sentence", as well as variations of "sentences", occur in phrase list. You can omit such variations by passing a scrubber function in the config.


```python
from spacy.tokens import Span
nlp = spacy.load("en_core_web_sm")


@spacy.registry.misc("prefix_scrubber")
def prefix_scrubber():
	def scrubber_func(span: Span) -> str:
		while span[0].text in ("a", "the", "their", "every", "other"):
			span = span[1:]
		return span.text
	return scrubber_func

nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] }, "scrubber": {"@misc": "prefix_scrubber"}})

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='sentences', chunks=[sentences, the sentences], count=2, rank=0.14407775200046075)
    ic| phrase: Phrase(text='Mihalcea et al', chunks=[Mihalcea et al], count=1, rank=0.11286475216345385)
    ic| phrase: Phrase(text='gensim implements TextRank', chunks=[gensim implements TextRank], count=1, rank=0.09589788430130489)
    ic| phrase: Phrase(text='text summarization', chunks=[text summarization], count=1, rank=0.09004754289053603)
    ic| phrase: Phrase(text='ranking webpages', chunks=[ranking webpages], count=1, rank=0.08473538778364878)
    ic| phrase: Phrase(text='sentence', chunks=[every sentence, every other sentence], count=2, rank=0.07909136977858265)
    ic| phrase: Phrase(text='Okapi BM25 function', chunks=[Okapi BM25 function], count=1, rank=0.07900911166567022)
    ic| phrase: Phrase(text='original TextRank', chunks=[original TextRank], count=1, rank=0.07165073049436399)
    ic| phrase: Phrase(text='TextRank', chunks=[TextRank, TextRank, TextRank, TextRank], count=4, rank=0.06888311869751775)
    ic| phrase: Phrase(text='two sentences', chunks=[the two sentences, two sentences], count=2, rank=0.06654666312136172)


Different variations of "sentence(s)" are now represented as part of single entry in phrase list.

As the scrubber takes in `Spans`, we can also use `toekn.pos_` or any other spaCy `Token` or `Span` attribute in the scrubbing. The variations of "sentences" have different DETs (determiners), so we could achieve a similar result with the folowing scrubber.


```python
@spacy.registry.misc("articles_scrubber")
def articles_scrubber():
    def scrubber_func(span: Span) -> str:
        for token in span:
            if token.pos_ not in ["DET", "PRON"]:
                break
            span = span[1:]
        return span.text
    return scrubber_func
```


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] }, "scrubber": {"@misc": "articles_scrubber"}})

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='sentences', chunks=[sentences, the sentences], count=2, rank=0.14407775200046075)
    ic| phrase: Phrase(text='Mihalcea et al', chunks=[Mihalcea et al], count=1, rank=0.11286475216345385)
    ic| phrase: Phrase(text='gensim implements TextRank', chunks=[gensim implements TextRank], count=1, rank=0.09589788430130489)
    ic| phrase: Phrase(text='text summarization', chunks=[text summarization], count=1, rank=0.09004754289053603)
    ic| phrase: Phrase(text='ranking webpages', chunks=[ranking webpages], count=1, rank=0.08473538778364878)
    ic| phrase: Phrase(text='other sentence', chunks=[every other sentence], count=1, rank=0.07909136977858265)
    ic| phrase: Phrase(text='Okapi BM25 function', chunks=[Okapi BM25 function], count=1, rank=0.07900911166567022)
    ic| phrase: Phrase(text='original TextRank', chunks=[original TextRank], count=1, rank=0.07165073049436399)
    ic| phrase: Phrase(text='TextRank', chunks=[TextRank, TextRank, TextRank, TextRank], count=4, rank=0.06888311869751775)
    ic| phrase: Phrase(text='sentence', chunks=[every sentence], count=1, rank=0.06654666312136172)


We could also use `Span` labels to filter out `ents`, for example, or certain types of entities, e.g. "CARDINAL", or "DATE", if need to do so for our use case.


```python
@spacy.registry.misc("entity_scrubber")
def articles_scrubber():
    def scrubber_func(span: Span) -> str:
        if span[0].ent_type_:
            # ignore named entities
            return "INELIGIBLE_PHRASE"
        return span.text
    return scrubber_func
```


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] }, "scrubber": {"@misc": "entity_scrubber"}})

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    if phrase.text != "INELIGIBLE_PHRASE":
        ic(phrase)
```

    ic| phrase: Phrase(text='sentences', chunks=[sentences], count=1, rank=0.14407775200046075)
    ic| phrase: Phrase(text='gensim implements TextRank', chunks=[gensim implements TextRank], count=1, rank=0.09589788430130489)
    ic| phrase: Phrase(text='text summarization', chunks=[text summarization], count=1, rank=0.09004754289053603)
    ic| phrase: Phrase(text='ranking webpages', chunks=[ranking webpages], count=1, rank=0.08473538778364878)
    ic| phrase: Phrase(text='every other sentence', chunks=[every other sentence], count=1, rank=0.07909136977858265)
    ic| phrase: Phrase(text='Okapi BM25 function', chunks=[Okapi BM25 function], count=1, rank=0.07900911166567022)
    ic| phrase: Phrase(text='original TextRank', chunks=[original TextRank], count=1, rank=0.07165073049436399)
    ic| phrase: Phrase(text='every sentence', chunks=[every sentence], count=1, rank=0.06654666312136172)
    ic| phrase: Phrase(text='the sentences', chunks=[the sentences], count=1, rank=0.06654666312136172)


## GraphViz Export

Let's generate a GraphViz doc `lemma_graph.dot` to visualize the *lemma graph* that **PyTextRank** produced for the most recent document...


```python
tr = doc._.textrank
tr.write_dot(path="lemma_graph.dot")
```


```python
!ls -lth lemma_graph.dot
```

    -rw-r--r--  1 paco  staff    17K Mar  6 14:39 lemma_graph.dot



```python
!pip install graphviz
```

    Requirement already satisfied: graphviz in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (0.17)


To render this graph, you must first download `GraphViz` <https://www.graphviz.org/download/>

Then you can render a `DOT` file...


```python
import graphviz as gv

gv.Source.from_file("lemma_graph.dot")
```




    
![svg](sample_files/sample_36_0.svg)
    



Note that the image which gets rendered in a notebook is probably "squished", but other tools can renders these as interesting graphs.

## Altair visualisation

Let's generate an interactive `altair` plot to look at the lemma graph.



```python
!pip install "altair"
```

    Requirement already satisfied: altair in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (4.1.0)
    Requirement already satisfied: entrypoints in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from altair) (0.3)
    Requirement already satisfied: jinja2 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from altair) (3.0.2)
    Requirement already satisfied: toolz in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from altair) (0.11.1)
    Requirement already satisfied: pandas>=0.18 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from altair) (1.3.3)
    Requirement already satisfied: jsonschema in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from altair) (4.1.0)
    Requirement already satisfied: numpy in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from altair) (1.21.2)
    Requirement already satisfied: python-dateutil>=2.7.3 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from pandas>=0.18->altair) (2.8.2)
    Requirement already satisfied: pytz>=2017.3 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from pandas>=0.18->altair) (2021.3)
    Requirement already satisfied: MarkupSafe>=2.0 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from jinja2->altair) (2.0.1)
    Requirement already satisfied: importlib-metadata in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from jsonschema->altair) (4.8.1)
    Requirement already satisfied: attrs>=17.4.0 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from jsonschema->altair) (21.2.0)
    Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from jsonschema->altair) (0.18.0)
    Requirement already satisfied: six>=1.5 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from python-dateutil>=2.7.3->pandas>=0.18->altair) (1.16.0)
    Requirement already satisfied: typing-extensions>=3.6.4 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from importlib-metadata->jsonschema->altair) (3.10.0.2)
    Requirement already satisfied: zipp>=0.5 in /Users/paco/src/pytextrank/venv/lib/python3.7/site-packages (from importlib-metadata->jsonschema->altair) (3.6.0)



```python
tr = doc._.textrank
tr.plot_keyphrases()
```





<div id="altair-viz-6d29793142bc4ab2be9ab6ce0a31f62f"></div>
<script type="text/javascript">
  (function(spec, embedOpt){
    let outputDiv = document.currentScript.previousElementSibling;
    if (outputDiv.id !== "altair-viz-6d29793142bc4ab2be9ab6ce0a31f62f") {
      outputDiv = document.getElementById("altair-viz-6d29793142bc4ab2be9ab6ce0a31f62f");
    }
    const paths = {
      "vega": "https://cdn.jsdelivr.net/npm//vega@5?noext",
      "vega-lib": "https://cdn.jsdelivr.net/npm//vega-lib?noext",
      "vega-lite": "https://cdn.jsdelivr.net/npm//vega-lite@4.8.1?noext",
      "vega-embed": "https://cdn.jsdelivr.net/npm//vega-embed@6?noext",
    };

    function loadScript(lib) {
      return new Promise(function(resolve, reject) {
        var s = document.createElement('script');
        s.src = paths[lib];
        s.async = true;
        s.onload = () => resolve(paths[lib]);
        s.onerror = () => reject(`Error loading script: ${paths[lib]}`);
        document.getElementsByTagName("head")[0].appendChild(s);
      });
    }

    function showError(err) {
      outputDiv.innerHTML = `<div class="error" style="color:red;">${err}</div>`;
      throw err;
    }

    function displayChart(vegaEmbed) {
      vegaEmbed(outputDiv, spec, embedOpt)
        .catch(err => showError(`Javascript Error: ${err.message}<br>This usually means there's a typo in your chart specification. See the javascript console for the full traceback.`));
    }

    if(typeof define === "function" && define.amd) {
      requirejs.config({paths});
      require(["vega-embed"], displayChart, err => showError(`Error loading script: ${err.message}`));
    } else if (typeof vegaEmbed === "function") {
      displayChart(vegaEmbed);
    } else {
      loadScript("vega")
        .then(() => loadScript("vega-lite"))
        .then(() => loadScript("vega-embed"))
        .catch(showError)
        .then(() => displayChart(vegaEmbed));
    }
  })({"config": {"view": {"continuousWidth": 400, "continuousHeight": 300}}, "data": {"name": "data-5a70d50020d6016af92c8759f37c158c"}, "mark": "bar", "encoding": {"color": {"type": "quantitative", "field": "count"}, "tooltip": [{"type": "nominal", "field": "text"}, {"type": "quantitative", "field": "rank"}, {"type": "quantitative", "field": "count"}], "x": {"type": "quantitative", "field": "index"}, "y": {"type": "quantitative", "field": "rank"}}, "title": "Keyphrase profile of the document", "$schema": "https://vega.github.io/schema/vega-lite/v4.8.1.json", "datasets": {"data-5a70d50020d6016af92c8759f37c158c": [{"index": 0, "text": "sentences", "count": 1, "rank": 0.14407775200046075}, {"index": 1, "text": "INELIGIBLE_PHRASE", "count": 21, "rank": 0.11286475216345385}, {"index": 2, "text": "gensim implements TextRank", "count": 1, "rank": 0.09589788430130489}, {"index": 3, "text": "text summarization", "count": 1, "rank": 0.09004754289053603}, {"index": 4, "text": "ranking webpages", "count": 1, "rank": 0.08473538778364878}, {"index": 5, "text": "every other sentence", "count": 1, "rank": 0.07909136977858265}, {"index": 6, "text": "Okapi BM25 function", "count": 1, "rank": 0.07900911166567022}, {"index": 7, "text": "original TextRank", "count": 1, "rank": 0.07165073049436399}, {"index": 8, "text": "every sentence", "count": 1, "rank": 0.06654666312136172}, {"index": 9, "text": "the sentences", "count": 1, "rank": 0.06654666312136172}, {"index": 10, "text": "the popular PageRank algorithm", "count": 1, "rank": 0.05335888932629289}, {"index": 11, "text": "vertices", "count": 1, "rank": 0.049900427583598826}, {"index": 12, "text": "implementations", "count": 1, "rank": 0.04843744036176572}, {"index": 13, "text": "the two sentences", "count": 1, "rank": 0.04832514712775797}, {"index": 14, "text": "the summarization module", "count": 1, "rank": 0.047089290608111706}, {"index": 15, "text": "an edge", "count": 2, "rank": 0.046108819024674536}, {"index": 16, "text": "the edge", "count": 1, "rank": 0.046108819024674536}, {"index": 17, "text": "an unsupervised algorithm", "count": 1, "rank": 0.04590933165691038}, {"index": 18, "text": "the highest PageRank score", "count": 1, "rank": 0.045894401837491466}, {"index": 19, "text": "another incubator student Olavur Mortensen", "count": 1, "rank": 0.044786361545027256}, {"index": 20, "text": "weighted-graphs", "count": 1, "rank": 0.0426755744719463}, {"index": 21, "text": "his previous post", "count": 1, "rank": 0.04254933225827145}, {"index": 22, "text": "the PageRank algorithm", "count": 1, "rank": 0.04050691407679936}, {"index": 23, "text": "the remaining words", "count": 1, "rank": 0.03802068505128614}, {"index": 24, "text": "this blog", "count": 1, "rank": 0.03778525440103907}, {"index": 25, "text": "-", "count": 1, "rank": 0.036368977979322474}, {"index": 26, "text": "top", "count": 1, "rank": 0.036368977979322474}, {"index": 27, "text": "some popular algorithms", "count": 1, "rank": 0.036106721162100744}, {"index": 28, "text": "the percentage", "count": 1, "rank": 0.03552664300233543}, {"index": 29, "text": "Pre", "count": 1, "rank": 0.03210407351764978}, {"index": 30, "text": "TextRank", "count": 1, "rank": 0.03210407351764978}, {"index": 31, "text": "a paper", "count": 2, "rank": 0.03024778334849052}, {"index": 32, "text": "the text", "count": 1, "rank": 0.028412169295393176}, {"index": 33, "text": "a graph", "count": 1, "rank": 0.024205867965342968}, {"index": 34, "text": "the graph", "count": 1, "rank": 0.024205867965342968}, {"index": 35, "text": "The weight", "count": 1, "rank": 0.019436270737826597}, {"index": 36, "text": "the weights", "count": 1, "rank": 0.019436270737826597}, {"index": 37, "text": "the vertices(sentences", "count": 1, "rank": 0.01679811138121072}, {"index": 38, "text": "an improvement", "count": 1, "rank": 0.014828236389998911}, {"index": 39, "text": "It", "count": 3, "rank": 0.0}, {"index": 40, "text": "both", "count": 1, "rank": 0.0}, {"index": 41, "text": "that", "count": 1, "rank": 0.0}, {"index": 42, "text": "them", "count": 1, "rank": 0.0}, {"index": 43, "text": "words", "count": 2, "rank": 0.0}]}}, {"mode": "vega-lite"});
</script>



## Extractive Summarization

Again, working with the most recent document above, we'll summarize based on its top `15` phrases, yielding its top `5` sentences...


```python
for sent in tr.summary(limit_phrases=15, limit_sentences=5):
    ic(sent)
```

    ic| sent: First, a quick description of some popular algorithms & implementations for text summarization that exist today: the summarization module in gensim implements TextRank, an unsupervised algorithm based on weighted-graphs from a paper by Mihalcea et al.
    ic| sent: Gensim’s TextRank uses Okapi BM25 function to see how similar the sentences are.
    ic| sent: Create a graph where vertices are sentences.
    ic| sent: It is built on top of the popular PageRank algorithm that Google used for ranking webpages.
    ic| sent: In original TextRank the weights of an edge between two sentences is the percentage of words appearing in both of them.


## Using TopicRank

The *TopicRank* enhanced algorithm is simple to use in the `spaCy` pipeline and it supports the other features described above:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("topicrank");
```

Let's load an example text:


```python
text = pathlib.Path("../dat/cfc.txt").read_text()
text
```




    " Chelsea 'opted against' signing Salomon Rondón on deadline day.\n\nChelsea reportedly opted against signing Salomón Rondón on deadline day despite their long search for a new centre forward. With Olivier Giroud expected to leave, the Blues targeted Edinson Cavani, Dries Mertens and Moussa Dembele – only to end up with none of them. According to Telegraph Sport, Dalian Yifang offered Rondón to Chelsea only for them to prefer keeping Giroud at the club. Manchester United were also linked with the Venezuela international before agreeing a deal for Shanghai Shenhua striker Odion Ighalo. Manager Frank Lampard made no secret of his transfer window frustration, hinting that to secure top four football he ‘needed’ signings. Their draw against Leicester on Saturday means they have won just four of the last 13 Premier League matches."




```python
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='Salomon Rondón', chunks=[Salomon Rondón, Salomón Rondón, Rondón], count=3, rank=0.07866221348202057)
    ic| phrase: Phrase(text='Chelsea', chunks=[Chelsea, Chelsea, Chelsea], count=3, rank=0.06832817272016853)
    ic| phrase: Phrase(text='Olivier Giroud', chunks=[Olivier Giroud, Giroud], count=2, rank=0.05574966582168716)
    ic| phrase: Phrase(text='deadline day', chunks=[deadline day, deadline day], count=2, rank=0.05008120527495589)
    ic| phrase: Phrase(text='Leicester', chunks=[Leicester], count=1, rank=0.039067778208486274)
    ic| phrase: Phrase(text='club', chunks=[club], count=1, rank=0.037625206033098234)
    ic| phrase: Phrase(text='Edinson Cavani', chunks=[Edinson Cavani], count=1, rank=0.03759951959121995)
    ic| phrase: Phrase(text='draw', chunks=[draw], count=1, rank=0.037353607917351345)
    ic| phrase: Phrase(text='Manchester United', chunks=[Manchester United], count=1, rank=0.035757812045215435)
    ic| phrase: Phrase(text='Dalian Yifang', chunks=[Dalian Yifang], count=1, rank=0.03570018233618092)


## Using PositionRank

The *PositionRank* enhanced algorithm is simple to use in the `spaCy` pipeline and it supports the other features described above:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("positionrank");
```


```python
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='deadline day', chunks=[deadline day, deadline day], count=2, rank=0.1671249044190727)
    ic| phrase: Phrase(text='Salomon Rondón', chunks=[Salomon Rondón, Salomon Rondón], count=2, rank=0.14836718147498046)
    ic| phrase: Phrase(text='Salomón Rondón', chunks=[Salomón Rondón, Salomón Rondón], count=2, rank=0.14169986334846618)
    ic| phrase: Phrase(text='Chelsea', chunks=[Chelsea, Chelsea, Chelsea, Chelsea, Chelsea, Chelsea], count=6, rank=0.13419811872859874)
    ic| phrase: Phrase(text='Rondón', chunks=[Rondón, Rondón], count=2, rank=0.12722264594603172)
    ic| phrase: Phrase(text='a new centre', chunks=[a new centre], count=1, rank=0.09181159181129885)
    ic| phrase: Phrase(text='Giroud', chunks=[Giroud, Giroud], count=2, rank=0.0783201596831592)
    ic| phrase: Phrase(text='Olivier Giroud', chunks=[Olivier Giroud, Olivier Giroud], count=2, rank=0.07805316118093475)
    ic| phrase: Phrase(text='none', chunks=[none], count=1, rank=0.07503538984105931)
    ic| phrase: Phrase(text='their long search', chunks=[their long search], count=1, rank=0.07449683199895643)


The top-ranked phrases from *PositionRank* are closely related to the "lead" items: `Chelsea`, `deadline day`, `Salomon Rondón`

## Baseline

Now let's re-run this pipeline with the baseline *TextRank* algorithm to compare results:


```python
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)
```

    ic| phrase: Phrase(text='Shanghai Shenhua striker Odion Ighalo', chunks=[Shanghai Shenhua striker Odion Ighalo], count=1, rank=0.11863090071749424)
    ic| phrase: Phrase(text='Odion Ighalo', chunks=[Odion Ighalo], count=1, rank=0.10925286108900635)
    ic| phrase: Phrase(text='none', chunks=[none], count=1, rank=0.09802416183300769)
    ic| phrase: Phrase(text='Moussa Dembele', chunks=[Moussa Dembele, Moussa Dembele], count=2, rank=0.09341044332809736)
    ic| phrase: Phrase(text='deadline day', chunks=[deadline day, deadline day], count=2, rank=0.09046182507994752)
    ic| phrase: Phrase(text='Dries Mertens', chunks=[Dries Mertens], count=1, rank=0.08919649435994934)
    ic| phrase: Phrase(text='Edinson Cavani', chunks=[Edinson Cavani, Edinson Cavani], count=2, rank=0.08418633972470349)
    ic| phrase: Phrase(text='Salomon Rondón', chunks=[Salomon Rondón, Salomon Rondón], count=2, rank=0.08228367707127111)
    ic| phrase: Phrase(text='Salomón Rondón', chunks=[Salomón Rondón, Salomón Rondón], count=2, rank=0.08228367707127111)
    ic| phrase: Phrase(text='Premier League', chunks=[Premier League], count=1, rank=0.08198820712767878)


The baseline algorithm is picking up named entities, although not emphasizing the order in which these entities were introduced in the text.
