import os
import csv
import requests
import pandas as pd

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(r'[^\w\s]', '', regex=True).str.replace(' ', '_')
    return df

def download_and_clean(url, filename):


    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

    df = pd.read_csv(filename)
    df = clean_column_names(df)

    df['city_state_zip'] = df['city_state_zip'].str.replace(r',(\S)', r', \1', regex=True)

    if 'violation_date' in df.columns:
        df['violation_date'] = pd.to_datetime(df['violation_date'], errors='coerce').dt.strftime('%Y/%m/%d')
    if 'resolved_date' in df.columns:
        df['resolved_date'] = pd.to_datetime(df['resolved_date'], dayfirst=True, errors='coerce').dt.strftime('%Y/%m/%d')
    
    df['id'] = range(1, len(df) + 1)
    df.to_csv(filename, index=False)

   

url = 'https://opendata.maryland.gov/api/views/tzjz-wfys/rows.csv?accessType=DOWNLOAD'
filename = 'static/solid_waste_violations.csv'


download_and_clean(url,filename)


