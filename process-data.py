import csv
import requests
from bs4 import BeautifulSoup

with open('data/chatdata.csv', 'r', newline='', encoding='mac_roman') as data_file:
    data = csv.reader(data_file, delimiter=',')

    for row in data:
        reply = row[1]
        if 'contact-us' in reply:
            label = 'General enquiry'
        else:
            url = 'http://www.nationalarchives.gov'+reply
            print(url)
            get_content = requests.get(url)
            get_text = get_content.text
            soup = BeautifulSoup(get_text, 'html.parser')
            label = soup.find_next('h1')

        print(label)

