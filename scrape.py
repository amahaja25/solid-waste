import os
import csv
import requests
import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep

def clean_column_names(df):
    df.columns = df.columns.str.lower().str.replace(r'[^\w\s]', '', regex=True).str.replace(' ', '_')
    return df

def download_and_clean(url, filename):


    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

    df = pd.read_csv(filename)
    df = clean_column_names(df)

    df['street_address'] = df['street_address'].str.replace(r'\bRoad\b', 'Rd', regex=True)
    df['street_address'] = df['street_address'].str.replace(r'\bLane\b', 'Ln', regex=True)


    df['city_state_zip'] = df['city_state_zip'].str.replace(r',(\S)', r', \1', regex=True)
    df['full_address'] = df['street_address'] + ', ' + df['city_state_zip']



    geolocator = Nominatim(user_agent="app.py")
    
    def geocode_address(full_address):
        try:
            location = geolocator.geocode(full_address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            return None, None

    df['latitude'] = None
    df['longitude'] = None

    for index, row in df.iterrows():
        lat, lon = geocode_address(row['full_address'])
        df.at[index, 'latitude'] = lat
        df.at[index, 'longitude'] = lon
        sleep(1)

    if 'violation_date' in df.columns:
        df['violation_date'] = pd.to_datetime(df['violation_date'], errors='coerce').dt.strftime('%Y/%m/%d')
    if 'resolved_date' in df.columns:
        df['resolved_date'] = pd.to_datetime(df['resolved_date'], dayfirst=True, errors='coerce').dt.strftime('%Y/%m/%d')
    
    df['id'] = range(1, len(df) + 1)
    df.to_csv(filename, index=False)

   

url = 'https://opendata.maryland.gov/api/views/tzjz-wfys/rows.csv?accessType=DOWNLOAD'
filename = 'static/solid_waste_violations.csv'


download_and_clean(url,filename)


