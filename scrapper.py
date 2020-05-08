from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
import re

browser = Browser("chrome", {"executable_path": "/usr/local/bin/chromedriver"}, headless=False)

def Mars_News(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(3)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html= browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
        time.sleep(3)
        slide_elem = soup.select_one("ul.item_list li.slide")
        titles= slide_elem.find("div", class_="content_title").get_text()
        paragraph = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return titles, paragraph
    
def image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    image_ele = browser.find_by_id('full_image')
    image_ele.click()
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_elem = browser.links.find_by_partial_text("more info")
    more_info_elem.click()

    html= browser.html
    soup = BeautifulSoup(html, "html.parser")
   
    img = soup.find('img', class_="main_image")
    try:
        image_url = img.get("src")
    except AttributeError:
    
        return None
    urls = f'https://www.jpl.nasa.gov{image_url}'
    return urls

def Hemisphere(browser):
    url = (
        "https://astrogeology.usgs.gov/search/"
        "results?q=hemisphere+enhanced&k1=target&v1=Mars"
    )
    browser.visit(url)
    hemisphere_image = []
    for i in range(4):
        browser.find_by_css("a.product-item h3")[i].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemisphere_image.append(hemi_data)
        browser.back()
    return hemisphere_image

def Twitter_Weather(browser):
    url = ("https://twitter.com/marswxreport?lang=en")

    browser.visit(url)
    time.sleep(4)
    html_browser = browser.html
    soup = BeautifulSoup(html_browser, 'html.parser')

    tweet = {"class": "tweet", "data-name": "Mars Weather"}
    mars_weather = soup.find("div", attrs=tweet)
    try:
        mars_weather = mars_weather.find("p", "tweet-text").get_text()
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = soup.find('span', text=pattern).text
    return mars_weather

def scrape_hemisphere(html_text):
    # Soupify the html text
    hemi_soup = BeautifulSoup(html_text, "html.parser")
    # Try to get href and text except if error.
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")
    except AttributeError:
        # Image error returns None for better front-end handling
        title_elem = None
        sample_elem = None
    hemisphere = {
        "title": title_elem,
        "img_url": sample_elem
    }
    return hemisphere

def Mars_Facts():
    try:
        facts_df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    facts_df.rename(columns={0: "Information", 1: "Values"})
    return facts_df.to_html(classes="table table-striped")

def scrapper():
    
    titles, paragraph = Mars_News(browser)

    data = {"News_Title": titles,
    "News Paragraph": paragraph,
    "Feature Images": image(browser),
    "Hemispheres": Hemisphere(browser),
    "Weather": Twitter_Weather(browser),
    "Facts": Mars_Facts(),
    "Last Modified": dt.datetime.now()
         }
    browser.quit()
    return data

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrapper())

    # print(image(browser))
    # browser.quit()
    


    
