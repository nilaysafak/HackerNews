from bs4 import BeautifulSoup
import requests

url = 'https://news.ycombinator.com'

response = requests.get(url = url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', {'id' : 'hnmain'})

table.find('table')

rows = table.find_all('tr', {'class': 'athing'})

for index, row in enumerate(rows, start = 1):
    
    span = row.find('span', {'class': 'titleline'})
    a = span.find('a')
    
    title = span.text
    url = a.get('href')
    
    print(f'[{index}] | {url} | {title}')