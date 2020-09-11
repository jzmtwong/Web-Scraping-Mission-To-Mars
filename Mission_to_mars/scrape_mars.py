# Declare Dependencies
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time

# create empty dictionary to store all info
mars_data = {}


# create path to access browser
def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_news():
    # NASA MARS NEWS

    # initialize browser
    browser = init_browser()

    # visit NASA news url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)  # visit news url
    time.sleep(5)
    html = browser.html
    soup = bs(html, 'html.parser')

    # get the first/latest element for news title / news_paragraph
    news_title = soup.find('div', class_='image_and_description_container').find('h3').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from MARS NEWS
    mars_data['news_title'] = news_title
    mars_data['news_paragraph'] = news_p

    # stop browser
    browser.quit()
    return mars_data

def scrape_image():
    # FEATURED IMAGE

    # initialize browser
    browser = init_browser()

    # visit Mars Space Images url
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(featured_image_url)  # Visit Mars Space Images url
    time.sleep(5)
    html_image = browser.html
    soup = bs(html_image, 'html.parser')

    # get background image from url with style tag
    image_url = soup.find('article')['style'].replace('background-image: url(', '').replace(');', '')[1:-1]

    # main page url
    main_url = 'https://www.jpl.nasa.gov'

    # combined url to get image url
    image_url = main_url + image_url

    # store in mars info
    mars_data['image_url'] = image_url
    # stop browser
    browser.quit()
    return mars_data

def scrape_facts():
    # MARS FACTS

    # initialize browser
    browser = init_browser()

    # visit website for mars facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    time.sleep(5)



    # parse the URL using pandas
    tables = pd.read_html(facts_url)
    # single out a table
    facts_df = tables[0]
    # assign the columns and format table with pandas
    facts_df.columns = ['Description', 'Value']
    html_table = facts_df.to_html(table_id="html_tbl_css", justify='left', index=False)

    # add mars facts to dictionary

    mars_data['tables'] = html_table
    # stop browser
    browser.quit()
    return mars_data

def scrape_hem():
    # Mars Hemisphere

    # initialize browser
    browser = init_browser()

    # Visit hemispheres website
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # html browser
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')
    time.sleep(5)

    # retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls
    hemispheres_image_urls = []

    # Store the main_ul
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    # Loop
    for i in items:
        # store title
        title = i.find('h3').text

        # store each link
        partial_img_url = i.find('a', class_='itemLink product-item')['href']

        # visit full image link
        browser.visit(hemispheres_main_url + partial_img_url)

        # HTML of each info url
        partial_img_html = browser.html

        # parse HTML for each url
        soup = bs(partial_img_html, 'html.parser')

        # retrieve full image
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']

        # create dictionary for each and append to stored list
        hemispheres_image_urls.append({"title": title, "img_url": img_url})

    mars_data['hemispheres_image_urls'] = hemispheres_image_urls

    # stop browser
    browser.quit()

    # return dictionary
    return mars_data


#####################################################################################
#scrape_news()
#scrape_image()
#scrape_facts()
scrape_hem()
print(mars_data)
