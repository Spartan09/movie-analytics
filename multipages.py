from bs4 import BeautifulSoup as bs
import requests
import pandas as pd 
from csv import writer
from google.colab import files

URL = ['https://www.eventbrite.com/d/india/business--events--this-month/?page=', 'https://www.eventbrite.com/d/india/business--events--next-month/?page=']

eventNames = []
eventDates = []
eventLocations = []

for url in URL:

    for page in range (1,9):

        page = requests.get(url + str(page)) 
        soup = bs(page.text , 'html.parser')
        lists = soup.find_all('div', class_="search-event-card-wrapper")


            
        
        for list in lists:
            Event_name = list.find('h3',class_ ="eds-event-card-content__title").text.replace('\n','')
            Date = list.find('div',class_="eds-event-card-content__sub-title").text.replace('\n','')
            Event_Location_Address = list.find('div',class_="card-text--truncated__one").text.replace('\n','')
            eventNames.append(Event_name)
            eventDates.append(Date)
            eventLocations.append(Event_Location_Address)

info = {'Event Name': eventNames, 'Date': eventDates, 'Event Location Address': eventLocations} 
df = pd.DataFrame(info)
df.to_csv('event.csv', header=True, index=False)
files.download('event.csv')
