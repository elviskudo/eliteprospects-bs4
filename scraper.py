import requests
from bs4 import BeautifulSoup
import json

def extract_team_data(url):
  """Extracts team data from a given URL using BeautifulSoup.

  Args:
      url: The URL of the webpage containing team data.

  Returns:
      A list of dictionaries, where each dictionary contains the following keys:
          title (str): The title of the team section (e.g., "Europe & Other - Men's Hockey").
          image_url (str): The URL of the image associated with the section (if available).
          teams (list): A list of dictionaries containing team details. Each team dictionary has the following keys:
              league (str): The league the team belongs to.
              team_link (str): The URL of the team's details page.
  """
  response = requests.get(url)
  soup = BeautifulSoup(response.content, 'html.parser')

  data = []
  sections = soup.find_all('header', class_='HocFrame_headerWithFunction__5EiCz')
  for section in sections:
    title = section.find('h2', class_='HocFrame_primaryTitle__uBTSP').text.strip()
    image_url = None
    image = section.find('img')
    if image:
      image_url = image.get('src')

    teams_list = []
    content = section.find_next_sibling(id=lambda id_: id_ and "table-list-content" in id_)
    if content:
      team_items = content.find_all('div', class_='LabelWithIcon_wrapper__Klo88')
      for team_item in team_items:
        team_link = team_item.find('a').get('href')
        league_text = team_item.find('a').text.strip()
        # Assuming league is indicated by text before the space
        league = league_text.split()[0]
        teams_list.append({
          'league': league,
          'team_link': team_link
        })

    data.append({
      'title': title,
      'image_url': image_url,
      'teams': teams_list
    })

  return data

# Get team data from the URL
team_data = extract_team_data('https://www.eliteprospects.com/teams')

# Write data to JSON file
with open('teams.json', 'w')  as outfile:
  json.dump(team_data, outfile)

print('Team data extracted and saved to teams.json successfully!')
