import networkx as nx
import csv
from pyvis.network import Network
import community as community_louvain

file = "authors_and_coauthors.csv"


G = nx.Graph()


with open(file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        author = row[0]
        co_authors = row[1].split(", ")
        for co_author in co_authors:
            G.add_edge(author, co_author)

communities = community_louvain.best_partition(G)
nx.set_node_attributes(G, communities, 'group')
# Create the network with Pyvis
node_degree = dict(G.degree)
nx.set_node_attributes(G, node_degree, 'size')
nx.set_node_attributes(G, node_degree, 'degree_centrality')
G1 = Network()
G1.from_nx(G)
G1.show('mygraph.html', notebook=False)
