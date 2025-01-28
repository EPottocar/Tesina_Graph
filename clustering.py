import networkx as nx
import pandas as pd
from geopy.distance import geodesic
import community as community_louvain
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import numpy as np

# 1. Caricamento dei dati
print("Caricamento dei dati...")
device_file = "Dati/nodiDevice.csv"
rilevazioni_file = "Dati/nodiRilevazioni.csv"
archi_file = "Dati/ArchiDeviceRilevazioni.csv"

devices = pd.read_csv(device_file)
rilevazioni = pd.read_csv(rilevazioni_file).sample(100, random_state=42)  # Campionamento casuale
archi = pd.read_csv(archi_file).sample(100, random_state=42)  # Campionamento casuale

print(f"Dispositivi caricati: {len(devices)}")
print(f"Rilevazioni caricate (campione casuale): {len(rilevazioni)}")
print(f"Archi caricati (campione casuale): {len(archi)}")

# 2. Creazione del grafo
print("Creazione del grafo...")
G = nx.Graph()

# Aggiungi nodi device
for _, row in devices.iterrows():
    G.add_node(row['id'], type='device', lat=row['latitude'], lon=row['longitude'])

# Aggiungi nodi rilevazioni
for _, row in rilevazioni.iterrows():
    G.add_node(row['id'], type='rilevazione', timestamp=row['Timestamp'], pm2_5=row['Pm2.5'])

# Aggiungi archi tra device e rilevazioni
for _, row in archi.iterrows():
    G.add_edge(row['source'], row['target'], weight=1)

print(f"Numero totale di nodi nel grafo: {G.number_of_nodes()}")
print(f"Numero totale di archi nel grafo: {G.number_of_edges()}")

# 3. Calcolo degli archi tra dispositivi vicini (KDTree per velocità)
print("Calcolo degli archi tra dispositivi vicini...")
device_coords = devices[['id', 'latitude', 'longitude']]
coords = device_coords[['latitude', 'longitude']].values
tree = cKDTree(coords)

radius = 50 / 6371  # Raggio in radianti
pairs = tree.query_pairs(radius, output_type='set')

for i, j in pairs:
    device1 = device_coords.iloc[i]['id']
    device2 = device_coords.iloc[j]['id']
    coord1 = (device_coords.iloc[i]['latitude'], device_coords.iloc[i]['longitude'])
    coord2 = (device_coords.iloc[j]['latitude'], device_coords.iloc[j]['longitude'])
    distance = geodesic(coord1, coord2).kilometers
    G.add_edge(device1, device2, weight=1 / (distance + 1))

print(f"Archi tra dispositivi aggiunti: {len(pairs)}")

# 4. Ottimizzazione per le rilevazioni con PM2.5 simile (usando KDTree per efficienza)
print("Calcolo degli archi tra rilevazioni con PM2.5 simile...")
pm2_values = rilevazioni[['id', 'Pm2.5']].values
tree_pm2 = cKDTree(pm2_values[:, 1].reshape(-1, 1))  # Crea KDTree basato su Pm2.5

threshold = 2  # Differenza massima consentita
pairs_pm2 = tree_pm2.query_pairs(threshold)

for i, j in pairs_pm2:
    node1 = int(pm2_values[i, 0])
    node2 = int(pm2_values[j, 0])
    diff = abs(pm2_values[i, 1] - pm2_values[j, 1])
    G.add_edge(node1, node2, weight=1 / (diff + 1))

print(f"Archi tra rilevazioni aggiunti: {len(pairs_pm2)}")

# 5. Applicazione del clustering (Louvain)
print("Esecuzione del clustering Louvain...")
partition = community_louvain.best_partition(G)
print(f"Numero di cluster trovati: {len(set(partition.values()))}")

# 6. Visualizzazione del grafo
print("Visualizzazione del grafo...")
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G,
    pos,
    node_color=[partition[node] for node in G.nodes()],
    with_labels=True,
    labels={node: node for node in G.nodes()},
    node_size=200,
    font_size=8,
    cmap=plt.cm.tab10
)

plt.title("Visualizzazione del grafo con clustering Louvain")
plt.show()

# 7. Esportazione dei risultati
output = pd.DataFrame({'node': list(partition.keys()), 'cluster': list(partition.values())})
output.to_csv("clustering_results.csv", index=False)
print("Risultati salvati in 'clustering_results.csv'")
