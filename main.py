import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://itc.gymkhana.iitb.ac.in/wncc/soc/'
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    names = [name.text for name in soup.find_all('p', class_='lead text-center font-weight-bold text-dark')]
    print(len(names))

    divs = soup.find_all('div', class_='rounded hover-wrapper pr-3 pl-3 pt-3 pb-3 bg-white')
    print(len(divs))

    rows = [[name, 'https://itc.gymkhana.iitb.ac.in' + d.get('href')] for name, d in zip(names, divs)]
    

    projDetails = []
    for row in rows:
        leads = []
        req = requests.get(row[1])
        soup = BeautifulSoup(req.content, 'html.parser')
        leads = [l.find('p', class_='lead').text for l in soup.find_all('li') if l.find('p', class_='lead') is not None]
        projDetails.append([row[0], row[1], ','.join(leads)])

    if projDetails:
        df = pd.DataFrame(projDetails, columns=['project', 'URL', 'mentors'])
        df.drop_duplicates(inplace=True)
        df.dropna(inplace=True)
        df.to_csv('soc_project_database.csv', index=False)
        print("Data extracted and saved successfully.")
    else:
        print("No data found.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
