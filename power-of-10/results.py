import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning


def find_event(event=None, meeting=None, venue=None, date_from=None, year=None, date_to=None, meeting_type=None, terrain=None):
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
        if meeting_type == 'UK Calendar':
            url += 'ukcalendar=y&'
        elif meeting_type == 'World Calendar':
            url += 'worldcalendar=y&'
        elif meeting_type == 'BMC':
            url += 'bmc=y&'
        elif meeting_type == 'NAL':
            url += 'meetingtypeid=53&'
        elif meeting_type == 'YDL':
            url += 'meetingtypeid=45&'
        elif meeting_type == 'SAL':
            url += 'meetingtypeid=44&'
        elif meeting_type == 'NEL':
            url += 'meetingtypeid=26&'
        elif meeting_type == 'MJL':
            url += 'meetingtypeid=34&'
    if terrain is not None:
        if terrain == 'any':
            url += 'terraintypecodes=A&'
        if terrain == 'virtual':
            url += 'terraintypecodes=V&'
        if terrain == 'disability':
            url += 'terraintypecodes=D&'
        if terrain == 'walks':
            url += 'terraintypecodes=W&'
        if terrain == 'mountain':
            url += 'terraintypecodes=H&'
        if terrain == 'fell':
            url += 'terraintypecodes=F&'
        if terrain == 'road/multi/xc':
            url += 'terraintypecodes=RMX&'
        if terrain == 'road/multi':
            url += 'terraintypecodes=RM&'
        if terrain == '5k/10k/hm/mar':
            url += 'terraintypecodes=B&'
        if terrain == 'xc':
            url += 'terraintypecodes=X&'
        if terrain == 'multi':
            url += 'terraintypecodes=M&'
        if terrain == 'indoor':
            url += 'terraintypecodes=I&'
        if terrain == 'road':
            url += 'terraintypecodes=R&'
        if terrain == 'track':
            url += 'terraintypecodes=T&'
        if terrain == 'track/10k/hm/mar/xc':
            url += 'terraintypecodes=TIDEX&'

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
    html = requests.get(url=url, params={'meetingid': meeting_id})
    soup = BeautifulSoup(html.text, 'html.parser')
    print(html.text)
    if 'Could not find meeting' in soup.find('div', {'id': 'pnlMainGeneral'}).text.replace('\n',''):
        raise ValueError('Meeting not found. Please input a valid meeting id')

    meeting_dets = soup.find('div', {'id': 'pnlMainGeneral'}).find_all('table')[0].find('span').find_all('span')
    meeting_res = soup.find('table', {'id': 'cphBody_dgP'})
    '''
    for i in meeting_res:
        print(i)
        print('-----------')
    '''
    for i in soup.find_all('div', {'id': 'pnlMainGeneral'}):
        print(i)
        print(' ----------- ')
    
    meeting = {
        'title': meeting_dets[0].text,
        'location': str(meeting_dets[1]).split('<br/>')[0].split('>')[1],
        'date': str(meeting_dets[1]).split('<br/>')[1].split('<')[0],
        'results': ''
    }
    #print(meeting)
    return

get_results(237786)