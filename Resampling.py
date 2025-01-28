import pandas as pd

df = pd.read_csv('Dati/idoSince2023.csv', sep=';')

# Convert the 'created_at_utc_original' column to datetime format
df['created_at_utc_original'] = pd.to_datetime(df['created_at_utc_original'], format='mixed')

# Round the timestamps to the nearest hour
df['created_at_utc_original'] = df['created_at_utc_original'].dt.round('H')

# Elimina le righe duplicate in base a 'created_at_utc_original' e 'device_id', tenendo solo la prima occorrenza
#df_unique = df.drop_duplicates(subset=['created_at_utc_original', 'device_id'], keep='first')

# Salva il DataFrame modificato in un nuovo file CSV
df.to_csv('Dati/idoSince2023_modified.csv', index=False)

# Stampa i primi 5 esempi della colonna
print(df['created_at_utc_original'].head())