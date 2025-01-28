import pandas as pd

# Carichiamo il file CSV
file_path = 'Dati/idoSince2023_modified.csv'
df = pd.read_csv(file_path)

# Troviamo le righe dove cambia il device_id
df['device_id_change'] = df['device_id'].ne(df['device_id'].shift()).cumsum()

# Raggruppiamo per ogni cambiamento di device_id, trovando le righe di inizio e fine
device_ranges = df.groupby('device_id_change').agg(
    device_id=('device_id', 'first'),
    start_row=('device_id', lambda x: x.index.min() + 1),
    end_row=('device_id', lambda x: x.index.max() + 1)
).reset_index(drop=True)

# Mostra i risultati
#print(device_ranges)

# Supponiamo che 'device_ranges' sia già definito
# Per ogni intervallo di device_id, creiamo le righe per il nuovo CSV
rows = []

# Itera attraverso device_ranges e crea i collegamenti da device_id a ciascun target (id rilevazione)
for _, row in device_ranges.iterrows():
    device_id = row['device_id']
    start_row = row['start_row']
    end_row = row['end_row']

    # Crea un arco per ciascuna rilevazione nell'intervallo
    for target in range(start_row, end_row + 1):
        rows.append({'source': device_id, 'target': target, 'type': 'directed'})

# Crea il nuovo dataframe
arcs_df = pd.DataFrame(rows)

# Salva il risultato in un file CSV
arcs_df.to_csv('Dati/ArchiDeviceRilevazioni_300.csv', index=False)

print("File ArchiDeviceRilevazioni.csv creato con successo.")


