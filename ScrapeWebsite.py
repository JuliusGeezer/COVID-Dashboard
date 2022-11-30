from bs4 import BeautifulSoup 
import pandas as pd
import requests
from pprint import pprint
import json
from datetime import datetime
import os

def scrape_country(url,country,stat=None):
    #Only works for worldometer. Enter worldometer url, a country name as a string, and an optional stat type such as "TotalDeaths". 
    #If stat is None, returns all relevant stats
    
    #find date to create new json file assosciating the date and data
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    filename = "worldometer-{}.json".format(date_str)
    data = None
    
    #Don't need to scrape website if the json file already exists so we will check for it 
    if os.path.isfile(filename):
 
        with open(filename,"r") as reader:
            data = json.load(reader)[country]
    else:
        #json file does not exist
        #https://python.plainenglish.io/scraping-covid-data-from-web-using-python-821397e0b83c
        #https://stackoverflow.com/a/42930782
        request = requests.get(url)
        #https://beautiful-soup-4.readthedocs.io/en/latest/
        soup = BeautifulSoup(request.content, 'html.parser')
        
        table = soup.find_all('table',id="main_table_countries_today")[0]

        #create data frame
        df = pd.read_html(str(table), displayed_only=False)[0]
        #removing "Total:" as it is unneeded. Leaves us with just the country names. set_index allows us to search by country name
        df = df.loc[df["Country,Other"] != "Total:"].set_index("Country,Other")
    
        #remove columns with unneeded data. Create dictionary from the filteres data. 
        #Country name is index, so all relevant data will appear for that specific country
        relevant_data = df[["TotalDeaths", "NewDeaths", "Deaths/1M pop","New Deaths/1M pop"]].to_dict(orient = "index")
    
        #creating json file
        #https://stackoverflow.com/a/12309296
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(relevant_data, f, ensure_ascii=False, indent=4)
        
        data = relevant_data[country]
    

    if stat == None:
        return data
    else:
        return data[stat]
    #print(relevant_data.loc[relevant_data["Country,Other"] == "Sweden","TotalDeaths"])
    

print(scrape_country("https://www.worldometers.info/coronavirus/", "Sweden","TotalDeaths"))
