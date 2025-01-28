import networkx as nx
import pandas as pd
import os

# Creo un grafo diretto utilizzando NetworkX
G = nx.DiGraph()

# Percorso del file di input
file_path = '../Dati/ArchiDeviceRilevazioni.csv'  # Modifica con il percorso corretto del tuo file
data = pd.read_csv(file_path)

# Aggiungo gli archi al grafo
for _, row in data.iterrows():
    G.add_edge(row['source'], row['target'])

# Percorso del file di output (nella cartella corrente)
output_path = os.path.join(os.getcwd(), '../archi.gexf')

# Salvo il grafo in formato .gexf
nx.write_gexf(G, output_path)

print(f"Grafo salvato correttamente nella cartella corrente: {output_path}")

