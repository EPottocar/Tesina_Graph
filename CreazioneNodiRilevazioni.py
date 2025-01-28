import pandas as pd

# Carico il file CSV caricato dall'utente
df = pd.read_csv('Dati/idoSince2023_modified.csv')

# Creo un nuovo DataFrame con le colonne richieste
rilevazioni_df = pd.DataFrame({
    'id': range(1, len(df) + 1),  # ID progressivo
    'Timestamp': pd.to_datetime(df['created_at_utc_original']).dt.strftime('%Y-%m-%dT%H:%M:%S'),  # Formato ISO 8601
    'Pm2.5': df['pm2p5_sps30_ug_m3']  # Campo Pm2.5
})

# Salvo il nuovo file CSV
output_file = 'Dati/nodiRilevazioni.csv'
rilevazioni_df.to_csv(output_file, index=False)

output_file



