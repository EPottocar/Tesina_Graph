import pandas as pd
import networkx as nx
import os

# Creare un grafo vuoto
G = nx.Graph()

# Specificare il percorso del file di input
file_path = 'Dati/nodiDevice.csv'  # Modifica con il percorso corretto del tuo file

# Leggere i dati dal file CSV
data = pd.read_csv(file_path)

# Aggiungere nodi al grafo con attributi
for _, row in data.iterrows():
    G.add_node(row['id'], longitude=row['longitude'], latitude=row['latitude'])

# Percorso del file di output (nella cartella corrente)
output_path = os.path.join(os.getcwd(), 'NodiDevice.gexf')

# Salvo il grafo in formato .gexf
nx.write_gexf(G, output_path)

print(f"Grafo salvato correttamente nel percorso: {output_path}")

