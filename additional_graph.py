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

# * Define the ERP Project name
erp_project_name = "bs_r&d_lab"

trello_cards_tup_ls = []
for card in cards:
    card_name = card["name"].lower()
    card_id = card["id"]
    trello_cards_tup_ls.append((card_name, card_id))

with open("erp_tasks.json", "r") as f:
    erp_tasks = json.load(f)

erp_tup_ls = create_erp_tupl_ls(erp_tasks)
cards_tupl_ls = create_cards_tupl_ls(cards)

trello_card_word_triples, trello_word_nodes = create_card_word_triples(cards, non_dc, nlp)
erp_task_word_triples, erp_task_word_nodes = create_card_word_triples(erp_tasks, non_dc, nlp)

# * Initialize Graph
graph = Graph(neo4j_url, name=neo4j_username, password=neo4j_password)
nodes_matcher = NodeMatcher(graph)

# * Add Board as a Node
add_nodes(graph, [(board_name.lower(), board_id)], labels={"Board"}, keys=["name", "board_id"])

# * Add ERP Project as a Node
add_nodes(graph, [(erp_project_name.lower(), "bs-erp")], labels={"ERPProject"}, keys=["name", "project_id"])

# * Add cards as Nodes
add_nodes(graph, trello_cards_tup_ls, labels={"TrelloCard"}, keys=["name", "id"])

# * Add trello tasks as Nodes
add_nodes(graph, erp_tup_ls, labels={"Task", "ERPtask"}, keys=["name", "from"])

# * Add card words as Nodes
add_nodes(graph, trello_word_nodes, labels={"Word", "CardWord"}, keys=["name", "card_name"])

# * Add erp task words as Nodes
add_nodes(graph, erp_task_word_nodes, labels={"Word", "ERPTaskWord"}, keys=["name", "task_name"])

# * Create edges
edge_tupl_ls = create_edges(board_name, cards_tupl_ls, card_word_triples=trello_card_word_triples, erp_tasks=erp_task_word_triples)

for task in erp_tup_ls:
    edge_tupl_ls["has"].append((erp_project_name, "has", task[0]))

add_edges(graph, nodes_matcher, Node, Relationship, edge_tupl_ls)