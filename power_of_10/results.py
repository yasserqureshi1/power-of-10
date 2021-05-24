import requests
from bs4 import BeautifulSoup
from .exceptions import QueryError, BroadQueryError



def search_event(event=None, meeting=None, venue=None, date_from=None, year=None, date_to=None, meeting_type=None, terrain=None):
    '''
    Returns a dict of events that correspond to the query parameters

            Parameters:
                    - 'event' (str): Optional event name
                    - 'meeting' (str): Optional meeting name
                    - 'venue' (str): Optional venue name
                    - 'date_from' (str): Optional date to search from (to be used with 'date_to')
                    - 'date_to' (str): Optional date to search to (to be used with 'date_from')
                    - 'year' (int): Optional year to search within
                    - 'meeting_type' (str): Optional type of meeting
                    - 'terrain' (str): Optional type of terrain event was on

            Returns:
                    - 'results' (arr): List of results corresponding to event parameters
                        - 'date' (str): Date of event
                        - 'meeting' (str): Meeting name
                        - 'venue' (str): Venue name of meeting
                        - 'type' (str): Type of terrain it was held on
                        - 'meeting_id' (int): Reference id of meeting (used by PowerOf10)
    '''
    url = 'https://www.thepowerof10.info/results/resultslookup.aspx?'

    if event is not None:
        url += f'event={str(event).replace(" ","+")}&'
    if meeting is not None:
        url += f'title={meeting.replace(" ","+")}&'
    if venue is not None:
        url += f'venue={venue.replace(" ","+")}&'
    if date_from is not None:
        url += f'datefrom={date_from}&'
    if date_to is not None:
        url += f'dateto={date_to}&'
    if year is not None:
        url += f'year={year}&'
    if meeting_type is not None:
        mt = {'UK Calendar': 'ukcalendar=y&', 'World Calendar': 'worldcalendar=y&', 'BMC': 'bmc=y&', 'NAL': 'meetingtypeid=53&', 'YDL': 'meetingtypeid=45&', 'SAL': 'meetingtypeid=44&', 'NEL': 'meetingtypeid=26&', 'MJL': 'meetingtypeid=34&'}
        url += mt[meeting_type]
    if terrain is not None:
        tt = {'any': 'terraintypecodes=A&', 'virtual': 'terraintypecodes=V&', 'disability': 'terraintypecodes=D&', 'walks': 'terraintypecodes=W&', 'mountain': 'terraintypecodes=H&', 'fell': 'terraintypecodes=F&', 'road/multi/xc': 'terraintypecodes=RMX&', 'road/multi': 'terraintypecodes=RM&', '5k/10k/hm/mar': 'terraintypecodes=B&', 'xc': 'terraintypecodes=X&', 'multi': 'terraintypecodes=M&', 'indoor': 'terraintypecodes=I&', 'road': 'terraintypecodes=R&', 'track': 'terraintypecodes=T&', 'track/10k/hm/mar/xc': 'terraintypecodes=TIDEX&'}
        url += tt[terrain]

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    try:
        table = soup.find('table', {'id': 'cphBody_dgMeetings'}).find_all('tr')
    except Exception as e:
        raise QueryError('No meetings found.')

    results = []
    for i in table:
        dets = i.find_all('td')
        if dets[0].text != 'Date':
            results.append({
                'date': dets[0].text,
                'meeting': dets[1].text.replace('\n','').replace('\r','').replace('     ','').replace('Info',''),
                'venue': dets[2].text,
                'type': dets[3].text,
                'meeting_id': str(dets[2]).split('"')[1].split('=')[1]
            })
            
    return results


def get_results(meeting_id):
    '''
    Returns a dict of information for a particular meeting 

            Parameters:
                    - 'meeting_id' (int): Reference id of meeting (used by PowerOf10)

            Returns:
                    - 'title' (str): Name of meeting
                    - 'location' (str): Location of meeting
                    - 'date' (str): Date of meeting
                    - 'results' (arr): List of results for each event at meeting
                        - 'event' (str): Event name
                        - 'age_group' (str): Age group that for event
                        - 'race' (int): Race number
                        - 'results' (arr): List of results for event
                            - 'pos' (int): Position of athlete
                            - 'perf' (float): Performance of athlete
                            - 'name' (str): Name of athlete
                            - 'athlete_id' (int): Reference id of athlete (used by PowerOf10) 
                            - 'age_group' (str): Age group division of athlete
                            - 'sex' (str): Gender of athlete 
                            - 'year' (str): Athlete year in age group
                            - 'coach' (str): Name of coach
                            - 'club' (str): Name of club
                            - 'sb' (float): Seasons best
                            - 'pb' (float): Personal best
    '''
    if meeting_id is None:
        raise QueryError('Please input a valud meeting id')

    url = f'https://www.thepowerof10.info/results/results.aspx?meetingid={meeting_id}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    if 'Could not find meeting' in soup.find('div', {'id': 'pnlMainGeneral'}).text.replace('\n','') or 'No results found' in soup.find('div', {'id': 'pnlMainGeneral'}).text.replace('\n',''):
        raise QueryError('Meeting not found. Please input a valid meeting id')

    meeting_dets = soup.find('div', {'id': 'pnlMainGeneral'}).find_all('table')[0].find('span')
    meeting_res = soup.find('table', {'id': 'cphBody_dgP'}).find_all('tr')[1:]

    results = []
    count = -1
    for i in meeting_res:
        dets = i.find_all('td')
        if len(dets) == 1 and '\xa0' not in str(dets[0]):
            vals = str(dets[0].text).split(" ")
            results.append({
                'event': vals[0],
                'age_group': vals[1],
                'race': vals[2] if len(vals)>2 else 1,
                'results': []
            })
            count += 1
            
        else:
            if '\xa0' not in str(dets[0]) and 'Pos' not in str(dets[0].text) :
                results[count]['results'].append({
                    'pos': dets[0].text,
                    'perf': dets[1].text,
                    'name': dets[2].text,
                    'athlete_id': str(dets[2]).split('"')[1].split('=')[1] if len(str(dets[2]).split('"')) > 1 else '',
                    'age_group': dets[4].text,
                    'gender': dets[5].text,
                    'year': dets[6].text,
                    'coach': dets[7].text if dets[7].text != '\xa0' else '',
                    'club': dets[8].text,
                    'sb': dets[9].text,
                    'pb': dets[10].text
                })

    meeting = {
        'title': str(meeting_dets).split('<b>')[1].split('</b')[0],
        'location': str(meeting_dets).split('<br/>')[1],
        'date': str(meeting_dets).split('<br/>')[2].split('</span>')[0],
        'results': results
    }
    
    return meeting


