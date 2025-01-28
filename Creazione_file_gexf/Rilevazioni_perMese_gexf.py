import pandas as pd
import networkx as nx
import os

# Carica il file CSV
file_path = '../Dati/nodiRilevazioni.csv'  # Modifica con il percorso corretto del tuo file
data = pd.read_csv(file_path)

# Converti la colonna Timestamp in formato datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Aggiungi una colonna per il mese e l'anno
data['YearMonth'] = data['Timestamp'].dt.to_period('M')

# Crea una cartella per i file GEXF
output_dir = '../gexf_files_mese/'
os.makedirs(output_dir, exist_ok=True)

# Raggruppa i dati per mese
grouped = data.groupby('YearMonth')

# Genera un file GEXF per ogni mese con la modifica richiesta
progressive_id = 1  # Contatore progressivo
for year_month, group in grouped:
    # Crea un grafo vuoto
    G = nx.DiGraph()  # Grafi diretti
    for _, row in group.iterrows():
        G.add_node(row['id'], Timestamp=row['Timestamp'].isoformat(), Pm2_5=row['Pm2.5'])

    # Nome temporaneo del file GEXF
    temp_filename = f"{output_dir}{year_month}_temp.gexf"
    nx.write_gexf(G, temp_filename)

    # Modifica il file GEXF per inserire la sezione <graph> personalizzata
    with open(temp_filename, 'r') as file:
        gexf_content = file.readlines()

    # Sostituisci la linea del tag <graph>
    for idx, line in enumerate(gexf_content):
        if '<graph ' in line:
            gexf_content[
                idx] = f'<graph mode="slice" defaultedgetype="directed" timerepresentation="timestamp" timestamp="{progressive_id}">\n'
            break

    # Scrivi il file finale
    final_filename = f"{output_dir}{year_month}.gexf"
    with open(final_filename, 'w') as file:
        file.writelines(gexf_content)

    # Rimuovi il file temporaneo
    os.remove(temp_filename)

    # Incrementa il contatore progressivo
    progressive_id += 1

print(f"File GEXF generati nella cartella: {output_dir}")



