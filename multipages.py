from bs4 import BeautifulSoup as bs
import requests
import pandas as pd 
from csv import writer

URL = 'https://www.eventbrite.com/d/india/business--events--this-month/?page='

for page in range (1,9):

    page = requests.get(URL + str(page)) 
    soup = bs(page.text , 'html.parser')
    lists = soup.find_all('div', class_="search-event-card-wrapper")


        
    
    for list in lists:
        Event_name = list.find('h3',class_ ="eds-event-card-content__title").text.replace('\n','')
        Date = list.find('div',class_="eds-event-card-content__sub-title").text.replace('\n','')
        Event_Location_Address = list.find('div',class_="card-text--truncated__one").text.replace('\n','')
        info = {Event_name, Date, Event_Location_Address} 
        print(info)  




    
