import pandas as pd

# Leggi il file CSV
input_file = "Dati/nodiDevice_modified.csv"  # Specifica il nome del file di input
output_file = "Dati/nodiDevice_modified.csv"  # Specifica il nome del file di output

# Carica i dati in un DataFrame
df = pd.read_csv(input_file)

# Controlla se le colonne 'start' e 'end' esistono
if 'start' in df.columns and 'end' in df.columns:
    # Crea la colonna 'interval'
    df['interval'] = df.apply(lambda row: f"[{row['start']}, {row['end']}]", axis=1)

    # Salva il nuovo DataFrame nel file di output
    df.to_csv(output_file, index=False)
    print(f"File con colonna 'interval' salvato come {output_file}")
else:
    print("Errore: il file deve contenere le colonne 'start' e 'end'")
