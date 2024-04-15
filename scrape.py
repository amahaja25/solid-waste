import requests

# writing thoughts for me to remember, i have to periodically download data from the same link so i can keep it updated, going to try and implement a similar thing to what i did in the umd alerts bot with the csv.

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

download_file('https://opendata.maryland.gov/api/views/tzjz-wfys/rows.csv?accessType=DOWNLOAD', 'solid_waste_violations')
