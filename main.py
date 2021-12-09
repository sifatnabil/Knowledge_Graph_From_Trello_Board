import json
from pprint import pprint
from py2neo import Node, Graph, Relationship, NodeMatcher

from helper import *
from graph_functions import *
from env import *

board_name = get_board_name(board_id)
cards = get_cards(board_id)
members = get_board_members(board_id)
checklists = get_checklists(board_id)
cards_with_checklists = get_cards_with_checklists(cards)

# * Create tuples of the above lists
members_tupl_ls = get_board_members_tupl_ls(members)
cards_tupl_ls = get_cards_tupl_ls(cards)
checklists_tupl_ls = get_checklists_tupl_ls(checklists)

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

# * Create edges dictionary for graph
edge_dc = create_edges(board_name, cards_tupl_ls, cards_with_checklists)

# * Add edges to the graph
add_edges(graph, nodes_matcher, Node, Relationship, edge_dc)
print("Successfully added edges to the graph")