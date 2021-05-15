import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning


def find_event(event=None, meeting=None, venue=None, date_from=None, year=None, date_to=None, meeting_type=None, terrain=None):
    '''
    Returns a list of events that correspond to the query parameters

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
                        - 'type' (str): <<<<<<<<<<<<<<<<
                        - 'meeting_id' (int): Reference id of meeting (used by PowerOf10)
    '''
    url = 'https://www.thepowerof10.info/results/resultslookup.aspx?'

    if event is not None:
        url += f'event={event}&'
    if meeting is not None:
        url += f'title={meeting}&'
    if venue is not None:
        url += f'venue={venue}&'
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

    table = soup.find('table', {'id': 'cphBody_dgMeetings'}).find_all('tr')

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
    # TODO: Fix get_results() function
    
    if meeting_id is None:
        raise ValueError('Please input a valud meeting id')

    url = f'https://www.thepowerof10.info/fixtures/meeting.aspx?meetingid={meeting_id}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    if 'Could not find meeting' in soup.find('div', {'id': 'pnlMainGeneral'}).text.replace('\n',''):
        raise ValueError('Meeting not found. Please input a valid meeting id')

    meeting_dets = soup.find('div', {'id': 'pnlMainGeneral'}).find_all('table')[0].find('span').find_all('span')
    meeting_res = soup.find('table', {'id': 'cphBody_dgP'})
    
    meeting = {
        'title': meeting_dets[0].text,
        'location': str(meeting_dets[1]).split('<br/>')[0].split('>')[1],
        'date': str(meeting_dets[1]).split('<br/>')[1].split('<')[0],
        'results': ''
    }
    #print(meeting)
    return
