from py2neo.bulk import merge_nodes 
from helper import get_card_members
from tqdm import tqdm

# * Add nodes to the graph
def add_nodes(graph, tup_ls, labels, keys):   
    merge_nodes(graph.auto(), tup_ls, ('Node', 'name'), labels=labels, keys=keys)
    print('Number of nodes in graph: ', graph.nodes.match('Node').count())


# * Create edges from erp
def create_erp_trello_edges(trello_cards_tupl, erp_words_tupl):
    edge_tupl = {}

    # * Edge between cards and words

    pass
    
# * Create edges for graph
def create_edges(board_name, cards_tupl, card_word_triples=None, checklist_word_triples=None, cards_with_checklists=None, synonym_triplets=None):
    edge_tupl = {}
    edge_ls = ["has"]

    # * Edge between board and cards
    for card in cards_tupl:
        if "has" in edge_tupl:
            edge_tupl["has"].append((board_name.lower(), "has", card[1]))
        else:
            edge_tupl["has"] = [(board_name.lower(), "has", card[1])]

    # * Edge between cards and checklists
    if cards_with_checklists:
        for card in cards_with_checklists:
            card_name = card['name'].lower()
            for checklist in card['checklists']:
                checklist_name = checklist['name'].lower()
                edge_tupl["has"].append((card_name, "has", checklist_name))

    # * Edge between members and cards
    for card in cards_tupl:
        card_id = card[0]
        card_name = card[1].lower()
        card_members = get_card_members(card_id)
        for member in card_members:
            member_name = member['fullName'].lower()
            edge_tupl["has"].append((card_name, "has", member_name))

    # * Edge between card and card words
    if card_word_triples:
        for item in card_word_triples:
            if item[1] in edge_tupl:
                edge_tupl[item[1]].append((item[0], item[1], item[2]))
            else:
                edge_tupl[item[1]] = [(item[0], item[1], item[2])]

    # * Edge between checklist and checklist words
    if checklist_word_triples:
        for item in checklist_word_triples:
            if item[1] in edge_tupl:
                edge_tupl[item[1]].append((item[0], item[1], item[2]))
            else:
                edge_tupl[item[1]] = [(item[0], item[1], item[2])]

    # * Edge between synonyms and words
    if synonym_triplets:
        for item in synonym_triplets:
            if item[1] in edge_tupl: 
                edge_tupl[item[1]].append((item[0], item[1], item[2]))
            else:
                edge_tupl[item[1]] = [(item[0], item[1], item[2])]
    
    return edge_tupl

# * Add edges between nodes
def add_edges(graph, nodes_matcher, Node, Relationship, edge_dc):
    for edge_labels, tup_ls in tqdm(edge_dc.items()):   # k=edge labels, v = list of tuples
        tx = graph.begin()
        
        for itr, el in enumerate(tup_ls):
            tx = graph.begin()
            source_node = nodes_matcher.match(name=el[0]).first()
            target_node = nodes_matcher.match(name=el[2]).first()
            if not source_node:
                source_node = Node('Node', name=el[0])
                print("Node not found, Source:", source_node )
                graph.create(source_node)
            if not target_node:
                try:
                    target_node = Node('Node', name=el[2], node_labels=el[4], url=el[5], word_vec=el[6])
                    print("Node not found, target:", source_node )
                    graph.create(target_node)
                except:
                    continue
            try:
                rel = Relationship(source_node, edge_labels, target_node)
            except:
                continue
            graph.create(rel)

        graph.commit(tx)