
import networkx as nx
import matplotlib.pyplot as plt
import csv
from pyvis.network import Network

file = "authors_and_coauthors.csv"
names = []

G = nx.Graph()

# Ouverture du fichier CSV et lecture des lignes
with open(file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        person1, person2 = row
        names.append((person1, person2))

# Ajout des arêtes au graphe
G.add_edges_from(names)

# Création du réseau avec pyvis
G1 = Network()
G1.from_nx(G)
G1.show('mygraph.html', notebook=False)

# Affichage du graphe avec NetworkX et Matplotlib
#nx.draw(G, with_labels=True)
#plt.show()
