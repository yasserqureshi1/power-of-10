import requests
from bs4 import BeautifulSoup
from .exceptions import QueryError, BroadQueryError

def search_coaches(firstname=None, surname=None, club=None):
    '''
    Returns a list of coaches with the inputted firstname, surname or club.

            Parameters:
                    - 'firstname' (str): Optional first name of coach argument
                    - 'surname' (str): Optiona surname of coach argument
                    - 'club' (str): Optional club of coach argument

            Returns:
                    - 'coaches' (arr): List of coach data in dict
                        - 'firstname' (str): First name of coach
                        - 'surname' (str): Surname of coach
                        - 'sex' (str): Gender of coach
                        - 'club' (str): Club of coach
                        - 'athlete_id' (int): reference id of athlete (used by PowerOf10)
    '''
    url = f'https://www.thepowerof10.info/coaches/coacheslookup.aspx?'
    if surname is not None:
        url += f'surname={surname.replace(" ","+")}&'
    if firstname is not None:
        url += f'firstname={firstname.replace(" ","+")}&'
    if club is not None:
        url += f'club={club.replace(" ","+")}'

    if firstname is None and surname is None and club is None:
        raise QueryError('Please input a firstname, surname or club')

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    if html.history != []:
        ath = html.url.split('=')[1]
        print(f'Only one athlete found with athlete_id: {ath}')
        return ath

    results = soup.find('div', {'id': 'cphBody_pnlResults'}).find_all('tr')

    if 'cphBody_lblResultsErrorMessage' in str(results[0]):
        raise QueryError(results[0].text)

    coaches = []
    for i in results[1:-1]:
        dets = i.find_all('td')
        coaches.append({
            'firstname': dets[0].text,
            'surname': dets[1].text,
            'sex': dets[2].text,
            'club': dets[3].text,
            'athlete_id': str(dets[4]).split('"')[1].split('=')[1]
        })

    return coaches

