import requests
from bs4 import BeautifulSoup
import re
import statistics
import matplotlib.pyplot as plt

heights_list = []
url = "http://www.espn.com/nfl/players/_/position/s"
html = requests.get(url).content
soup = BeautifulSoup(html, 'html.parser')

links = []
table = soup.find('table', {'class': 'tablehead'})
rows = table.findAll('tr')
for tr in rows:
    cols = tr.findAll('td')
    atags = cols[0].findAll('a')
    for atag in atags:
        links.append(atag.get('href'))

for link in links:
    player_html = requests.get(link).content
    new_soup = BeautifulSoup(player_html, 'html.parser')
    general_player_info = new_soup.find('ul', {'class': 'general-info'})
    info_pieces = general_player_info.findAll('li')
    player_height = str(info_pieces[1])
    height_feet = re.search("<li>(.)\W\s", player_height).group(1)
    height_inches = re.search("\s(.+?)\W\W\s", player_height).group(1)
    total_height_inches = int(height_feet) * 12 + int(height_inches)
    heights_list.append(total_height_inches)
    print total_height_inches

print statistics.pstdev(heights_list)
print statistics.mean(heights_list)

bins_intervals = []
interval = 65
while interval < 80:
    bins_intervals.append(interval)
    interval = interval + 1
plt.hist(heights_list, bins=bins_intervals)
plt.show()
