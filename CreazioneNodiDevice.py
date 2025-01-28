import pandas as pd

df = pd.read_csv('Dati/idoSince2023_modified.csv')

# Group by 'device_id' and extract the first and last date for each device
nodi_df = df.groupby('device_id').agg(
    longitude=('longitude', 'first'),
    latitude=('latitude', 'first'),
    #start=('created_at_utc_original', 'min'),
    #end=('created_at_utc_original', 'max')
).reset_index()

# Convert 'start' and 'end' columns to datetime format
#nodi_df['start'] = pd.to_datetime(nodi_df['start']).dt.strftime('%Y-%m-%dT%H:%M:%S')
#nodi_df['end'] = pd.to_datetime(nodi_df['end']).dt.strftime('%Y-%m-%dT%H:%M:%S')

# Create 'interval' column in the format <[start, end]>
#nodi_df['interval'] = '<[' + nodi_df['start'] + ', ' + nodi_df['end'] + ']>'

# Drop 'start' and 'end' columns
#nodi_df = nodi_df.drop(columns=['start', 'end'])

# Rename 'device_id' column to 'id'
nodi_df = nodi_df.rename(columns={'device_id': 'id'})

# Save the resulting DataFrame to a new CSV file called 'nodiDevice.csv'
output_path = 'Dati/nodiDevice.csv'
nodi_df.to_csv(output_path, index=False)

# Show the new DataFrame
nodi_df.head(), output_path



