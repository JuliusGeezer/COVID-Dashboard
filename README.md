# COVID-Dashboard
Kenny Ho u1117236
Daniel Webster u1437452

How to run web scrape:
Call the scrape_country function. There are three total inputs, one mandatory, and two optional. 
You must input the url for the worldometer website. It is provided on the comments of the code, if you do not have it.
The second input is an optional country input. Inputting this will retrieve the stats associated with that counrty.
If it is not given, the function will output stats for all countries. Third is an optional stat input. Here you can
request a specific stat. Type in "TotalDeaths", "NewDeaths", "Deaths/1M pop", or "New Deaths/1M pop" as these are the
available stats. Without this input, the function will return all the stats for the given country. Otherwise,
it will only output the requested stat for that country.

Examples:
print(scrape_country("https://www.worldometers.info/coronavirus/", "Sweden", "TotalDeaths"))
print(scrape_country("https://www.worldometers.info/coronavirus/", "Cameroon"))
print(scrape_country("https://www.worldometers.info/coronavirus/"))

These examples are all valid inputs.

How to run project (data display):
Step 1. download all files
step 2. run DataDisplay to bring up html

DataDisplay description:
left plot is a line plot to show the covid deaths in each continent. Lines can be hidden by clicking labels on the legend. 
middle plot is a line plot of all the countries, continents, and world. 
right plot is a bar graph of covid data for a few different countries. Click on the tabs above the plot to switch the data on the bar graph. 
