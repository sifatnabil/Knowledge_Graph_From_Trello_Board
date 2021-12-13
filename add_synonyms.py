import nltk
from nltk.corpus import wordnet 

nltk.download('wordnet')

def find_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word.lower()):
        for l in syn.lemmas():
            synonyms.append(l.name().lower())
    return synonyms

def add_synonyms(entities):
    synonym_nodes = []
    entity_synonyms = {}
    synonym_triplets = []

    for ent in entities:
        synonyms = find_synonyms(ent['n.name'])
        entity_synonyms[ent['n.name']] = synonyms
        synonyms = set(synonyms)
        if synonyms:
            for syn in synonyms:
                synonym_nodes.append((syn, ent['n.name']))
                synonym_triplets.append((ent['n.name'], 'is_synonym_of', syn))

    return synonym_nodes, entity_synonyms, synonym_triplets