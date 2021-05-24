import requests
from bs4 import BeautifulSoup
from .exceptions import QueryError, BroadQueryError

def get_rankings(year, gender, age_group, event, region=None):
    '''
    Returns a list of ranks for given year, region, gender, age group and event.

            Parameters:
                    - 'year' (int): Year of event rankings 
                    - 'region' (str): Region for event rankings
                    - 'gender' (str): Gender for event rankings
                    - 'age_group' (str): Age group of event rankings
                    - 'event' (str): Event for rankings

            Returns:
                    - 'rankings' (arr): list of ranks
                        - 'rank' (int): Rank of athlete
                        - 'performance' (float): Performance of athlete for given rank
                        - 'pb' (float): Personal best of athlete at time of rank
                        - 'name' (str): Full name of athlete
                        - 'year' (int): Year that performance occurred
                        - 'coach' (str): Name of coach of athlete
                        - 'club' (str): Name of club of athlete
                        - 'venue' (str): Name of venue that performance occurred
                        - 'date' (str): Date that performance occurred
                        - 'athlete_id' (int): Reference id of athlete (used by PowerOf10)
                        - 'meeting_id' (int): Reference id of event (used by PowerOf10)
    '''
    if None in (year, region, gender, age_group, event):
        raise QueryError('Please ensure all search fields are filled.')

    url = f'https://www.thepowerof10.info/rankings/rankinglist.aspx?event={event.replace(" ","+")}&agegroup={age_group}&sex={gender}&year={year}'
    
    locs = {'east': 66, 'east midlands': 65, 'england': 91, 'london': 67, 'north east': 61, 'north ireland': 94, 
    'north west': 63, 'scotland': 92, 'south east': 68, 'south west': 69, 'wales': 93, 'west midlands': 64, 'yorkshire': 62}
    if region is not None:
        try:
            url += f'&areaid={locs[region.lower()]}'
        except Exception as e:
            raise QueryError('Please ensure the location you have provided is valid.')
        
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    results = []
    try:
        results = soup.find('span', {'id': 'cphBody_lblCachedRankingList'}).find_all('tr')
    except Exception as e:
        QueryError('Please ensure all fields are filled correctly.')

    rankings = []
    for i in results[2:]:
        dets = i.find_all('td')
        if dets[0].text != '' and len(dets) > 11:
            rankings.append({
                'rank': dets[0].text,
                'performance': dets[1].text,
                'pb': dets[4].text,
                'name': dets[6].text,
                'year': dets[8].text,
                'coach': dets[9].text,
                'club': dets[10].text,
                'venue': dets[11].text,
                'date': dets[12].text,
                'athlete_id': str(dets[6]).split('"')[1].split('=')[1],
                'meeting_id': str(dets[11]).split('=')[2].split('&')[0]
            })
    
    return rankings