from bs4 import BeautifulSoup as bs
import requests
import pandas as pd 
import numpy as np
from csv import writer

URL = ['https://www.eventbrite.com/d/india/business--events--this-month/?page=', 'https://www.eventbrite.com/d/india/business--events--next-month/?page=']

eventNames = []
eventDates = []
eventTimes = []
eventDescriptions = []
eventLocations = []

for url in URL:

    for page in range (1,9):

        page = requests.get(url + str(page)) 
        soup = bs(page.text , 'html.parser')
        lists = soup.find_all('div', class_="search-event-card-wrapper")
        # lists = soup.find_all('a', class_="eds-event-card-content__action-link")
        # lists = soup.find('a', class_='eds-event-card-content__action-link', href=True)
        
        for list in lists:
            cardURL = list.find('a', class_='eds-event-card-content__action-link')['href']
            cardPage = requests.get(cardURL) 
            cardParser = bs(cardPage.text , 'html.parser')

            #Event Name
            Event_name = cardParser.find('h1',class_ ="listing-hero-title").text.replace('\n','')

            eventDetailContent = cardParser.find('div', class_="event-detail__content")
            eventDetailAllContent = cardParser.find_all('div', class_="event-detail__content")

            #Event Date
            # Date = list.find('div',class_="eds-event-card-content__sub-title").text.replace('\n','')
            eventDetail = eventDetailContent
            if eventDetail and eventDetail.find('time'):
                timeDetails = eventDetail.find('time').find_all('p')
                date = timeDetails[0].text.replace('\n','')
                time = timeDetails[1].text.replace('\n','')
                # print(f'Event: {Event_name}, date: {date}, time: {time} ')
            else:
                date = 'Online'
                time = 'Online'

            #Event Address
            eventAddressCardEl = eventDetailAllContent[1]
            if eventAddressCardEl:
                addressEls = eventAddressCardEl.find_all('p')[:-1]
                address = ''
                for addressEl in addressEls:
                    address += addressEl.text.replace('\n','') + ', '
                    address = address[:-2]
                print(f'Event: {Event_name}, address: {address}')
            elif not eventAddressCardEl and not eventDetail.find('time'):
                eventAddressCardEl = eventDetailAllContent[0]
                addressEls = eventAddressCardEl.find_all('p')[:-1]
                address = ''
                for addressEl in addressEls:
                    address += addressEl.text.replace('\n','') + ', '
                    address = address[:-2]
                print(f'Event: {Event_name}, address: {address}')
            else:
                address += 'N/A'

            #Event Description
            descriptionHolder = cardParser.find('div', class_ = "eds-text--left")
            # print(descriptionHolder)
            if descriptionHolder:
                description = descriptionHolder.find('p').text.replace('\n', " ")
            else:
                description = 'N/A'


            eventNames.append(Event_name)
            eventDates.append(date)
            eventTimes.append(time)
            eventLocations.append(address)
            eventDescriptions.append(description)


# #To CSV
info = {'Event': eventNames, 'Date': eventDates, 'Time': eventTimes, 'Address': eventLocations, 'Description': eventDescriptions} 
df = pd.DataFrame(info)
df.to_csv('event.csv', header=True, index=False)

#To JSON
df.to_json('event.json')

