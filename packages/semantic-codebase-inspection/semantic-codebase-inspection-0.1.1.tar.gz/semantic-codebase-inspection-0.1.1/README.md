# Semantic Codebase Inspection

SCI helps developers familiarize themselves with a python project that has decent naming conventions.

It requires the libraries: 

tensorflow-text
tensorflow-hub
inspect

It downloads an NLP model of about 300MB.

https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3

It uses a Natural Language Processing model to turn the names of functions, classes, and variables (variables that outside of functions) into vectors. Queries can be submitted against those names which don't need to be exact matches. Currently, the language model being used accommodates 16 languages, which means it accommodates synonyms too. This is accomplished with technology related to word2vec, doc2vec, and embeddings. If this seems somehow magic to you, I encourage you to read more about it so that you can be a magician too because it's not that complicated.

```python3
>> import semantic_codebase_inspection
>> semantic_codebase_inspection.run_semantic_search_through_program()
(printed) Importing modules and semantic model.

(printed) What module would you like to explore?
(input) requests

(printed) What function in the library are you interesting in exploring?
(input) get

(printed) How many objects would you like in your result? (integer answers only)
(input) 5

*waiting for search to execute*

Similar semantic candidates include:
get : get function
put : put function
__build__ :   build   int 
__url__ :   url   str 
post : post function
```

Exit with ctrl+C.