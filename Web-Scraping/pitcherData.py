import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver

years = [i for i in range(1960, 2019)]
runOnce = True
# os.remove('scrapeData.txt')

for year in years:
    requestBaseURL = 'https://www.baseball-reference.com/leagues/MLB/'
    scrapPageURL = str(year) + '-standard-pitching.shtml'
    fullURL = requestBaseURL + '/' + scrapPageURL

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(fullURL)
    html = driver.page_source.encode('UTF-8')
    driver.close()

    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('div', attrs={'id': 'div_players_standard_pitching'})
    results = results.findChild('tbody')
    results = results.findAll('tr')

    results = list(results)

    f = open('pitcherScrapeData.txt', 'a')

    for result in results:
        if runOnce:
            headers = [tag['data-stat'] for tag in result]
            headers.append('year')
            f.write(','.join(headers) + '\n')
            runOnce = False
        if result['class'][0] != 'thead' and result['class'][0] != 'league_average_table':
            # print(result['class'])
            data = [tag.text.replace("\u00A0"," ") for tag in result]
            data.append(str(year))
            f.write(','.join(data) + '\n')

    f.close()

