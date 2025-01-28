import pandas as pd
import networkx as nx
import os
import pytz

# Carica il file CSV
file_path = '../Dati/nodiRilevazioni.csv'  # Modifica con il percorso corretto del tuo file
data = pd.read_csv(file_path)

# Carica le date come datetime senza fuso orario
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Aggiungi il fuso orario di Roma (Europe/Rome) gestendo le date non esistenti e ambigue
rome_tz = pytz.timezone('Europe/Rome')
data['Timestamp'] = data['Timestamp'].dt.tz_localize(rome_tz, ambiguous='NaT', nonexistent='shift_forward')  # Gestione ore non esistenti

# Gestisci i valori NaT nella colonna Timestamp
data['Timestamp_epoch'] = data['Timestamp'].apply(
    lambda x: int(x.timestamp()) if pd.notna(x) else None  # Verifica se x è NaT
)

# Rimuovi righe con NaT nei timestamp (opzionale, puoi scegliere un altro metodo di gestione)
data = data.dropna(subset=['Timestamp_epoch'])

# Aggiungi una colonna per raggruppare per anno, mese, giorno e ora
data['YearMonthDayHour'] = data['Timestamp'].dt.to_period('H')  # Raggruppamento per ora
data['YearMonth'] = data['Timestamp'].dt.to_period('M')  # Raggruppamento per mese
data['YearMonthDay'] = data['Timestamp'].dt.to_period('D')  # Raggruppamento per giorno

# Crea una cartella principale per i file GEXF
output_dir = '../gexf_file_ore/'
os.makedirs(output_dir, exist_ok=True)

# Raggruppa i dati per ogni ora
grouped = data.groupby('YearMonthDayHour')

# Genera un file GEXF per ogni ora
for year_month_day_hour, group in grouped:
    # Ottieni il timestamp epoch
    timestamp_epoch = int(group.iloc[0]['Timestamp_epoch'])  # Utilizza il timestamp già calcolato
    year_month = group.iloc[0]['Timestamp'].strftime('%Y-%m')  # Es. '2025-01'
    year_month_day = group.iloc[0]['Timestamp'].strftime('%Y-%m-%d')  # Es. '2025-01-24'

    # Crea le sottocartelle per mese e giorno
    month_dir = os.path.join(output_dir, year_month)  # Cartella del mese
    day_dir = os.path.join(month_dir, year_month_day)  # Cartella del giorno
    os.makedirs(day_dir, exist_ok=True)

    # Crea un grafo vuoto
    G = nx.DiGraph()  # Grafi diretti
    for _, row in group.iterrows():
        G.add_node(row['id'], Timestamp=row['Timestamp'].isoformat(), Pm2_5=row['Pm2.5'])

    # Nome del file GEXF
    final_filename = f"{day_dir}/{timestamp_epoch}.gexf"
    nx.write_gexf(G, final_filename)

    # Modifica il file GEXF per inserire la sezione <graph> personalizzata
    with open(final_filename, 'r') as file:
        gexf_content = file.readlines()

    # Sostituisci la linea del tag <graph>
    for idx, line in enumerate(gexf_content):
        if '<graph ' in line:
            gexf_content[
                idx
            ] = f'<graph mode="slice" defaultedgetype="directed" timerepresentation="timestamp" timestamp="{timestamp_epoch}">\n'
            break

    # Sovrascrivi il file con il contenuto modificato
    with open(final_filename, 'w') as file:
        file.writelines(gexf_content)

print(f"File GEXF generati nella cartella: {output_dir}")
