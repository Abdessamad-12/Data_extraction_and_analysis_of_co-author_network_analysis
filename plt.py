import csv
import networkx as nx
import matplotlib.pyplot as plt

# Charger les données depuis le fichier CSV
authors_data = []
with open('authors_and_coauthors.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        authors_data.append(row)

# Créer le graphe de co-auteurs
G = nx.Graph()

for data in authors_data:
    author = data['Author']
    co_authors = data['Co-authors'].split(', ')
    for co_author in co_authors:
        G.add_edge(author, co_author)

# Visualiser le graphe
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, k=0.1)  # Positionnement des nœuds
nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
plt.title('Réseau de co-auteurs')
plt.show()
