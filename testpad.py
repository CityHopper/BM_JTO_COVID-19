import nltk
from nltk.corpus import wordnet as wn

tab = "    "
for synset in wn.synsets('kindle'):
    print("{}:".format(synset.name()))
    print(tab+"definition: {}".format(synset.definition()))
    print(tab+"pos: {}".format(synset.pos()))
    for e in synset.examples():
        print("    "+"example: {}".format(e))
    print()

for synset in wn.synsets('car'):
    print("{}: {}".format(synset.name(), synset.definition()))
    synonyms = ", ".join([lem.name() for lem in synset.lemmas()])
    print(tab + "synonyms: {}".format(synonyms))

    hypernyms = ", ".join([hypernym.name() for hypernym in synset.hypernyms()])
    print(tab + "hypernyms: {}".format(hypernyms))
    print()