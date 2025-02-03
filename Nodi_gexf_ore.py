import pandas as pd
import networkx as nx
import os

# Carica i dati aggiornati
file_path = '../Dati/idoSince2023_modified.csv'  # Nuovo file CSV con latitudine e longitudine
data = pd.read_csv(file_path)

# Rinomina le colonne per uniformità
data.rename(columns={'created_at_utc_original': 'Timestamp', 'device_id': 'id', 'pm2p5_sps30_ug_m3': 'Pm2_5'}, inplace=True)

# Carica le date come datetime
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Gestisci i valori NaT nella colonna Timestamp
data['Timestamp_epoch'] = data['Timestamp'].apply(lambda x: int(x.timestamp()) if pd.notna(x) else None)

# Rimuovi righe con NaT nei timestamp
data = data.dropna(subset=['Timestamp_epoch'])

# Raggruppa per anno, mese, giorno e ora
data['YearMonthDayHour'] = data['Timestamp'].dt.to_period('H')  # Per ora
data['YearMonth'] = data['Timestamp'].dt.to_period('M')  # Per mese
data['YearMonthDay'] = data['Timestamp'].dt.to_period('D')  # Per giorno

# Elimina duplicati mantenendo solo la prima rilevazione per ogni dispositivo per ora
data = data.drop_duplicates(subset=['id', 'YearMonthDayHour'], keep='first')

# Crea la cartella per i file GEXF
output_dir = '../gexf_file_ore/'
os.makedirs(output_dir, exist_ok=True)

# Raggruppa i dati per ogni ora
grouped = data.groupby('YearMonthDayHour')

# Genera un file GEXF per ogni ora
for year_month_day_hour, group in grouped:
    timestamp_epoch = int(group.iloc[0]['Timestamp_epoch'])  # Timestamp per il file
    year_month = group.iloc[0]['Timestamp'].strftime('%Y-%m')  # Es. '2025-01'
    year_month_day = group.iloc[0]['Timestamp'].strftime('%Y-%m-%d')  # Es. '2025-01-24'

    # Crea le cartelle
    month_dir = os.path.join(output_dir, year_month)
    day_dir = os.path.join(month_dir, year_month_day)
    os.makedirs(day_dir, exist_ok=True)

    # Crea il grafo
    G = nx.DiGraph()

    # Aggiungi i nodi con attributi
    for _, row in group.iterrows():
        G.add_node(
            row['id'],
            Timestamp=row['Timestamp'].isoformat(),
            Pm2_5=row['Pm2_5'],  # Ora si usa pm2_5
            Latitude=row['latitude'],  # Aggiunta latitudine
            Longitude=row['longitude'],  # Aggiunta longitudine
        )

    # Aggiungi archi tra tutti i nodi (peso = 1)
    node_ids = group['id'].tolist()
    for i in range(len(node_ids)):
        for j in range(i + 1, len(node_ids)):  # Evita autoloop
            G.add_edge(node_ids[i], node_ids[j], weight=1)

    # Nome del file GEXF
    final_filename = f"{day_dir}/{timestamp_epoch}.gexf"
    nx.write_gexf(G, final_filename)

    # Modifica il file GEXF per personalizzare il tag <graph>
    with open(final_filename, 'r') as file:
        gexf_content = file.readlines()

    for idx, line in enumerate(gexf_content):
        if '<graph ' in line:
            gexf_content[idx] = f'<graph mode="slice" defaultedgetype="directed" timerepresentation="timestamp" timestamp="{timestamp_epoch}">\n'
            break

    with open(final_filename, 'w') as file:
        file.writelines(gexf_content)

print(f"File GEXF generati nella cartella: {output_dir}")