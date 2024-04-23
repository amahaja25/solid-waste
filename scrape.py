import os
import requests
import pandas as pd
import uuid
from playwright.sync_api import sync_playwright
import shutil

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(r'[^\w\s]', '', regex=True).str.replace(' ', '_')
    return df

def download_and_clean(url, filename):

    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

    df = pd.read_csv(filename)
    df = clean_column_names(df)

    df['uuid'] = [str(uuid.uuid4()) for _ in range(len(df))]

    df.to_csv(filename, index=False)

url = 'https://opendata.maryland.gov/api/views/tzjz-wfys/rows.csv?accessType=DOWNLOAD'
filename = 'solid_waste_violations.csv'

download_and_clean(url, filename)
