import requests
from bs4 import BeautifulSoup

def find_coaches(firstname=None, surname=None, club=None):
    url = f'https://www.thepowerof10.info/coaches/coacheslookup.aspx?'
    if surname is not None:
        url += f'surname={surname}&'
    if firstname is not None:
        url += f'firstname={firstname}&'
    if club is not None:
        url += f'club={club}'

    if firstname is None and surname is None and club is None:
        raise ValueError('Please input a firstname, surname or club')

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    results = soup.find('table', {'id': 'cphBody_dgCoaches'}).find_all('tr')

    coaches = []
    for i in results[1:]:
        dets = i.find_all('td')
        coaches.append({
            'firstname': dets[0].text,
            'surname': dets[1].text,
            'sex': dets[2].text,
            'club': dets[3].text,
            'athlete_id': str(dets[4]).split('"')[1].split('=')[1]
        })

    return coaches

