# power-of-10: A UK Athletics API

This library intends to provide simplicity when accessing and parsing data from <a href="https://www.thepowerof10.info">Power of 10</a>, a UK-based site that provides a comprehensive collection of athete performances and rankings.

## Installation

Install the package:
```
pip install setup.py
```

Install dependencies:
```
pip install -r requirements.txt
```

## Usage

The package has a variety of functions.

### 1. Search Athletes
```
search_athletes(firstname=None, surname=None, club=None)
```
Returns a list of athletes given search criteria.

*Parameters:*
- `firstname` (str): Optional first name agrument
- `surname` (str): Optional surname argument
- `club` (str): Optional club agrument

*Returns:*
- `list_of_athletes` (arr): List of athlete data in dict
    - `firstname` (str): First name of athlete
    - `surname` (str): Surname of athlete
    - `track` (str): Age group for athlete on track 
    - `road` (str): Age group for athlete on road
    - `sex` (str): Gender of athlete
    - `club` (str): Athletics club of althete
    - `athlete_id` (int): Reference id of athlete (used by PowerOf10)


### 2. Get Athlete
```
get_athlete(athlete_id)
```
Returns a dictionary of information relating to a specific athlete or coach.

*Parameters:*
- `athlete_id` (int): reference id of athlete (used by PowerOf10)

*Returns:*
- `athletes` (dict): Dictionary of athlete data
    - `club` (str): Club of the athlete
    - `gender` (str): Gender of athlete (M or F)
    - `age_group` (str): Age group division of athlete
    - `county` (str): County that athlete competes for
    - `region` (Str): Region that athlete competes for
    - `nation` (str): Nation that athlete competes for
    - `lead coach` (str): Athlete coach (usually used for notable coaches)
    - `about` (str): Description of athlete (usually used for notable athletes)
    - `pb` (arr): List of personal bests
        - `event` (str): Event name
        - `value` (float): Personal best in given event
        - `performances` (arr): List of athlete performances
        - `event` (str): Event name
        - `value` (float): Performance in given event
        - `position` (arr): 2x1 list containing [position, race identifier]
        - `venue` (str): Location of event
        - `meeting` (str): Meeting title
        - `date` (str): Date of event
    - `rankings` (arr): List of notable ranks of athletes
        - `event` (str): Event name
        - `age_group` (str): Age group division at time of rank
        - `year` (int): Year that rank was achieved
        - `rank` (int): Rank of athlete
    - `coaching` (arr): List of coaching experiences 
        - `name` (str): Nmae of athlete coached
        - `club` (str): Club of athlete coached
        - `age_group` (str): Age group division of athlete coached
        - `sex` (str): Gender of athlete coached
        - `best_event` (str): Best event of athlete coached
        - `rank` (int): Rank of athlete coached for their best event
        - `age_group_rank` (str): Age group that rank was achieved
        - `year` (int): Year that rank was achieved
        - `performance` (float): Performance that achieved rank

### 3. Find Coaches
```
search_coaches(firstname=None, surname=None, club=None)
```
Returns a list of coaches with the inputted firstname, surname or club.

*Parameters:*
- `firstname` (str): Optional first name of coach argument
- `surname` (str): Optiona surname of coach argument
- `club` (str): Optional club of coach argument

*Returns:*
- `coaches` (arr): List of coach data in dict
    - `firstname` (str): First name of coach
    - `surname` (str): Surname of coach
    - `sex` (str): Gender of coach
    - `club` (str): Club of coach
    - `athlete_id` (int): reference id of athlete (used by PowerOf10)

### 4. Get Rankings
```
get_rankings()
```
Returns a list of ranks for given year, region, gender, age group and event.

*Parameters:*
- `year` (int): Year of event rankings 
- `region` (str): Region for event rankings (see below for available regions)
- `gender` (str): Gender for event rankings
- `age_group` (str): Optional age group of event rankings
- `event` (str): Event for rankings

*Returns:*
- `rankings` (arr): list of ranks
    - `rank` (int): Rank of athlete
    - `performance` (float): Performance of athlete for given rank
    - `pb` (float): Personal best of athlete at time of rank
    - `name` (str): Full name of athlete
    - `year` (int): Year that performance occurred
    - `coach` (str): Name of coach of athlete
    - `club` (str): Name of club of athlete
    - `venue` (str): Name of venue that performance occurred
    - `date` (str): Date that performance occurred
    - `athlete_id` (int): Reference id of athlete (used by PowerOf10)
    - `meeting_id` (int): Reference id of event (used by PowerOf10)

**Table of Parameters:**
Region | Age Group 
-------|-----------
east | Leave blank for any 
east midlands | U20 
england | U17 
london | U15  
north east | U13 
north ireland | | 
north west | | 
scotland | | 
south east | | 
south west | | 
wales | | 
west midlands | | 
yorkshire | | 

### 5. Search Event
```
search_event(event=None, meeting=None, venue=None, date_from=None, year=None, date_to=None, meeting_type=None, terrain=None)
```
Returns a dict of events that correspond to the query parameters

*Parameters:*
- `event` (str): Optional event name
- `meeting` (str): Optional meeting name
- `venue` (str): Optional venue name
- `date_from` (str): Optional date to search from (to be used with `date_to`)
- `date_to` (str): Optional date to search to (to be used with `date_from`)
- `year` (int): Optional year to search within
- `meeting_type` (str): Optional type of meeting (See below for available meeting types)
- `terrain` (str): Optional type of terrain event was on

*Returns:*
- `results` (arr): List of results corresponding to event parameters
    - `date` (str): Date of event
    - `meeting` (str): Meeting name
    - `venue` (str): Venue name of meeting
    - `type` (str): Type of terrain it was held on
    - `meeting_id` (int): Reference id of meeting (used by PowerOf10)

**Table of Parameters:**
Terrain Types | Meeting Types
-------|-----------
any | UK Calendar
virtual | World Calendar
disability | BMC
walks | NAL
mountain | YDL 
fell | SAL
road/multi/xc | NEL
road/multi | MJL
5k/10k/hm/mar | 
xc | 
multi | 
indoor | 
road | 
track | 
track/10k/hm/mar/xc |

### 6. Get Results
```
get_results(meeting_id)
```
Returns a dict of information for a particular meeting 

*Parameters:*
- `meeting_id` (int): Reference id of meeting (used by PowerOf10)

*Returns:*
- `meeting` (arr):
    - `title` (str): Name of meeting
    - `location` (str): Location of meeting
    - `date` (str): Date of meeting
    - `results` (arr): List of results for each event at meeting
        - `event` (str): Event name
        - `age_group` (str): Age group that for event
        - `race` (int): Race number
        - `results` (arr): List of results for event
            - `pos` (int): Position of athlete
            - `perf` (float): Performance of athlete
            - `name` (str): Name of athlete
            - `athlete_id` (int): Reference id of athlete (used by PowerOf10) 
            - `age_group` (str): Age group division of athlete
            - `sex` (str): Gender of athlete 
            - `year` (str): Athlete year in age group
            - `coach` (str): Name of coach
            - `club` (str): Name of club
            - `sb` (float): Seasons best
            - `pb` (float): Personal best

