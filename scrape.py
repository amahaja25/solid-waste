import os
import csv
import requests
import pandas as pd

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(r'[^\w\s]', '', regex=True).str.replace(' ', '_')
    return df

def download_and_clean(url, filename):

    if os.path.exists(filename):
        existing_data = pd.read_csv(filename)
    else:
        existing_data = pd.DataFrame()

    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

    new_data = pd.read_csv(filename)
    new_data = clean_column_names(new_data)

    new_data['city_state_zip'] = new_data['city_state_zip'].str.replace(r',(\S)', r', \1', regex=True)

    if 'violation_date' in new_data.columns:
        new_data['violation_date'] = pd.to_datetime(new_data['violation_date'], errors='coerce').dt.strftime('%Y/%m/%d')

    if 'resolved_date' in new_data.columns:
        new_data['resolved_date'] = pd.to_datetime(new_data['resolved_date'], dayfirst=True, errors='coerce').dt.strftime('%Y/%m/%d')

    
    new_data['id'] = range(len(existing_data) + 1, len(existing_data) + 1 + len(new_data))

    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    combined_data.to_csv(filename, index=False)

url = 'https://opendata.maryland.gov/api/views/tzjz-wfys/rows.csv?accessType=DOWNLOAD'
filename = 'static/solid_waste_violations.csv'


download_and_clean(url,filename)


