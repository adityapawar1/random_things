import nba_id
import requests
from bs4 import BeautifulSoup as bs

name = input('Enter the name of the player you want to find in this format: FirstName LastName\n')
fn, ln = name.split(' ')

player_id = nba_id.find(fn.title(), ln.title())

print(player_id)

url = 'https://stats.nba.com/player/' + player_id + '/'
if not player_id == 'Not Found':
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    stats = soup.find_all('span', attrs={'class':"player-stats__stat-value"})[::2]
    title = soup.find_all('div', attrs={'class':'player-stats__stat-title'})[::2]
    [print('{} {}'.format(title[c].text, stat.text)) for c, stat in enumerate(stats)]
    
