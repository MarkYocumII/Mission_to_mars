#import BeautifulSoup
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from splinter import Browser
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


browser = init_browser()
#Mars.nasa.gov scrape
#import webpage to be scraped, use requests module to obtain webpage URL and parse with beautifulsoup
url = 'https://mars.nasa.gov/news/'

#visit url and get html from new browser (bypass Javascript), use BeautifulSoup parser
browser.visit(url)
html = browser.html
soup = bs(html, 'html.parser')

#find all results with content-title within div
results = soup.find_all('div', class_="content_title")

#find first title
news_title = results[0].text
print(news_title)

#first first paragraph body associated with title
p_results = soup.find_all('div', class_="article_teaser_body")
news_p = p_results[0].text
print(news_p)
browser.quit()

#jpl.nasa.gov scrape
#assign url and visit
browser = init_browser()
jp_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(jp_url)

#click through to full image
browser.click_link_by_partial_text('FULL IMAGE')

#define img site url from open browser after clicking on full image
img_html = browser.html
img_soup = bs(img_html, 'html.parser')

#find all articles
result_1 = img_soup.find_all("article")
# print(result_1[0].prettify())

#img link is attribute withing article within data-fancybox-href
img_link = result_1[0].a["data-fancybox-href"]    

#define base url
base_img_url = "https://www.jpl.nasa.gov"

#combined base url with specific image url
featured_img_url = base_img_url + img_link
print(featured_img_url)
browser.quit()

#mars weather scrape
#assign url and visit
browser = init_browser()
t_url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(t_url)
t_html = browser.html
t_soup = bs(t_html, 'html.parser')

#find results that contain tweet stream
t_results = t_soup.find_all('div', class_="js-tweet-text-container")
# print(t_results[0].prettify())

#look through results to find first paragraph entry that contains 'Insight sol' as key for weather data, if found then break the loop and store string
for result in t_results:
    p_text = result.p.text
    key_string = "InSight sol"
    if key_string not in p_text:
        continue
    else: mars_weather = p_text
    break

print(mars_weather)
browser.quit()

#mars facts scrape
fact_url = "http://space-facts.com/mars/"

#read in tables as html via PANDAS
tables = pd.read_html(fact_url)

#mars facts is only table on page, so 0th dataframe element is table list
mars_facts_df = tables[0]

#rename columns to parameter and value to clean up dataframe
mars_facts_df = mars_facts_df.rename(columns={0:"Paramter", 1:"Value"})

#convert dataframe to html string
mars_html_table = mars_facts_df.to_html()
print(mars_html_table)

#ASGS scrape
#assign url and visit
browser = init_browser()

#visit main page
usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(usgs_url)

#define html from main page and parse
usgs_html = browser.html
usgs_soup = bs(usgs_html, 'html.parser')

#find results for each item
usgs_results = usgs_soup.find_all('div', class_="item")
# len(usgs_results)

hemisphere_image_urls = []

for i in range(0, len(usgs_results)):
    #find title via h3 header, strip out word "Enhanced"
    title = usgs_results[i].find('h3').text.strip("Enhanced")
        
    #find image url - locate enhanced image url and open new browser
    image_url = usgs_results[i].a["href"]
    base_url = "https://astrogeology.usgs.gov"
    enhanced_url = base_url + image_url
    browser.visit(enhanced_url)
    
    #create new base line html from new enhanced image in browser
    sample_html = browser.html
    sample_soup = bs(sample_html, 'html.parser')
    
    #find link within class of downloads - sample results will only return one item
    sample_results = sample_soup.find_all('div', class_="downloads")
    img_url = sample_results[0].a["href"]

    #add title and image url to dictionary
    dict_img = {"title": title, "img url": img_url}
    hemisphere_image_urls.append(dict_img)

print(hemisphere_image_urls)

#store mars data in a dictionary
mars_data = {
    "news_title" : news_title,
    "news_p" : news_p,
    "featured_img_url" : featured_img_url,
    "mars_weather" : mars_weather,
    "mars_html_table" : mars_html_table,
    "hemisphere_img_list" : hemisphere_image_urls
}

browser.quit()
