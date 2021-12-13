import json
import spacy
from pprint import pprint
from py2neo import Node, Graph, Relationship, NodeMatcher

from helper import *
from graph_functions import *
from env import *
from add_synonyms import add_synonyms

# * Load Spacy Pipeline
non_dc = spacy.load('en_core_web_md')
nlp = spacy.load('en_core_web_md')
nlp.add_pipe('merge_noun_chunks')

# * Get necessary data from trello  
board_name = get_board_name(board_id)
cards = get_cards(board_id)
members = get_board_members(board_id)
checklists = get_checklists(board_id)
cards_with_checklists = get_cards_with_checklists(cards)

card_word_triples, word_nodes = create_card_word_triples(cards, non_dc, nlp)
checklist_word_triples, checklist_word_nodes = create_checklist_word_triples(cards, non_dc, nlp)

# * Create tuples of the above lists
members_tupl_ls = create_board_members_tupl_ls(members)
cards_tupl_ls = create_cards_tupl_ls(cards)
checklists_tupl_ls = create_checklists_tupl_ls(checklists)

# * Initialize Graph
graph = Graph(neo4j_url, name=neo4j_username, password=neo4j_password)
nodes_matcher = NodeMatcher(graph)

# * Add Board as a Node
add_nodes(graph, [(board_name.lower(), board_id)], labels={"Board"}, keys=["name", "board_id"])
print("Added Board as a Node")

# * Add Board Members as Nodes
add_nodes(graph, members_tupl_ls, labels={"Person"}, keys=["user_id", "name", "username"])
print("Added Board Members as Nodes")

# * Add cards as Nodes
add_nodes(graph, cards_tupl_ls, labels={"Card"}, keys=["card_id", "name", "description" "url"])
print("Added cards as nodes")

# * Add checklists as Nodes
add_nodes(graph, checklists_tupl_ls, labels={"Checklist"}, keys=["checklist_id", "name", "state"])
print("Added checklists as nodes")

# * Add card words words as Nodes
add_nodes(graph, word_nodes, labels={"Word", "CardWord"}, keys=["name", "card_name", "card_url"])

# * Add checklist words as Nodes
add_nodes(graph, checklist_word_nodes, labels={"Word", "ChecklistWord"}, keys=["name", "card_name", "checklist_name", "card_url"])

# * Find Synonyms and Add them as nodes
entities = graph.run("MATCH (n:Word) RETURN n.name").data()
synonym_nodes, entity_synonyms, synonym_triplets = add_synonyms(entities)
add_nodes(graph, synonym_nodes, labels={"Synonym"}, keys=["name", "synonym_of"])

# * Create edges dictionary for graph
edge_tupl_ls = create_edges(board_name,         
                            cards_tupl_ls, 
                            card_word_triples, 
                            checklist_word_triples, 
                            cards_with_checklists, 
                            synonym_triplets)

# * Add edges to the graph
add_edges(graph, nodes_matcher, Node, Relationship, edge_tupl_ls)
print("Successfully added edges to the graph")