import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from geopy.distance import geodesic

# Carica i dati dei device (sensori) e delle rilevazioni
device_df = pd.read_csv("Dati/nodiDevice.csv")  # id, longitudine, latitudine
rilevazioni_df = pd.read_csv("Dati/nodiRilevazioni.csv")  # id, timestamp, pm2.5, longitudine, latitudine

# Assicurati che il timestamp sia in formato datetime
rilevazioni_df['timestamp'] = pd.to_datetime(rilevazioni_df['timestamp'])

# Funzione per associare ogni rilevazione al device più vicino
def find_nearest_device(row, devices):
    rilevazione_coords = (row['latitudine'], row['longitudine'])
    devices['distance'] = devices.apply(
        lambda device: geodesic(rilevazione_coords, (device['latitudine'], device['longitudine'])).meters,
        axis=1
    )
    nearest_device = devices.loc[devices['distance'].idxmin()]
    return nearest_device['id']

# Associa ogni rilevazione al device più vicino
rilevazioni_df['device_id'] = rilevazioni_df.apply(
    find_nearest_device, axis=1, devices=device_df
)

# Ordina i dati per device e timestamp
rilevazioni_df = rilevazioni_df.sort_values(by=['device_id', 'timestamp'])

# Funzione per interpolare i valori PM2.5 mancanti
def interpolate_pm25(data):
    if data['pm2.5'].notna().sum() > 1:
        interp_func = interp1d(
            data['timestamp'].astype(np.int64),  # Converti il timestamp in numeri interi
            data['pm2.5'],
            kind='linear',
            bounds_error=False,
            fill_value='extrapolate'
        )
        data['pm2.5'] = interp_func(data['timestamp'].astype(np.int64))
    return data

# Applica l'interpolazione per ogni device
rilevazioni_interpolated = rilevazioni_df.groupby('device_id').apply(interpolate_pm25)

# Salva i risultati in un nuovo CSV
rilevazioni_interpolated.to_csv('rilevazioni_interpolated.csv', index=False)

print("Interpolazione completata. Risultati salvati in 'rilevazioni_interpolated.csv'.")
