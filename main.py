from bs4 import BeautifulSoup
import requests
import lxml
import pandas as pd

base_url = "https://www.fifaindex.com/players/updated/?order=0&order_by=overallrating"

requests.get(base_url)

#Send get http request
page = requests.get(base_url)
#print(type(page))

print(page.status_code)

#ensure successful webpage call
if page.status_code == requests.codes.ok:
  #get page in beautiful soup format
  bs = BeautifulSoup(page.text, 'lxml')

#find something you specify in the html
player_names = bs.select('td[data-title="Name"]')

#print (player_names[:10])

data = {
  'Name': [],
  'Team': [],
  'OVR / POT': []
}

#print(player_names[0].next_sibling.next_sibling.next_sibling.next_sibling.title)

list_of_players = player_names[:10]

#print (list_of_players[0]['title'].split(" ")[0]+" "+list_of_players[0]['title'].split(" ")[1])

for player in list_of_players:
  name = player.text
  team = player.next_sibling.next_sibling.next_sibling.next_sibling.find('a')['title']
  rating = player.previous_sibling.text
  
  if name:
    data['Name'].append(name)
  else:
    data['Name'].append("n/a")
  if team:
    data['Team'].append(team)
  else:
    data['Team'].append("n/a")
  if rating:
    data['OVR / POT'].append(rating[:2]+' / '+rating[2:])
  else:
    data['OVR / POT'].append("n/a")

table = pd.DataFrame(data,columns=['Name','Team','OVR / POT'])
table.index+= 1
print(table)
table.to_csv('top_ten_soccer_players.csv',sep=',',encoding='utf-8')


