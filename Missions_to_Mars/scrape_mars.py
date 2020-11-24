# These are a couple of functions to grab the data from the nasa website on mars.
# We have used/tested this code in Jupyter Notebook and are bringing it 
# all together here.  It will go to the website and scrape data for the headline
# information and it's summary paragraph.  Then if grabs an image from a different
# portion of the website.  Next it scrapes for a table of data.  Finally, it gets 
# a number of images.  All of these will be used to create our own website to 
# summarize some Mars data.


from splinter import Browser
from bs4 import BeautifulSoup 
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    # Rather than hvaing a a single function, I'm going to create 4 which 
    # do the individual pieces, then call each of them in this main function
    # This is essentially the same code as the Jupyter Notebook code, 
    # though it passes data differently.
    headline = news_headline()
    body = news_body()
    featured_image_url = image()
    tables = FAQs()
    images = hemispheres()
    print(body)
    
    mars_data = {
        "headline": headline,
        "body": body,
        "featured_image_url": featured_image_url,
        "tables": tables,
        "images": images
    }
    print(tables)

    return mars_data

def news_headline():
    # this is the function which will get the news_title and news_paragraph 
    # start by initiating the browser
    browser = init_browser()
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html1 = browser.html 
    soup1 = BeautifulSoup(html1, 'lxml')
    # Article title/headline here, under div/content_title in the soup
    articles_list = soup1.find_all('div', class_ = 'content_title')
    headline = articles_list[1].a.text
    return headline

def news_body():
    # this is the function which will get the news_title and news_paragraph 
    # start by initiating the browser
    browser = init_browser()
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    html1 = browser.html 
    soup1 = BeautifulSoup(html1, 'lxml')
    # Article title/headline here, under div/content_title in the soup
    body_list = soup1.find('div', class_='article_teaser_body').text

    return body_list
# headline_test = news()
# print(headline_test)

def image():
    # go to the website where the image is
    browser = init_browser()
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    # got to the page where the fav image is 
    browser.links.find_by_partial_text('FULL IMAGE').click()
    # get the url for the featured image, start with creating a soup for it
    html2 = browser.html 
    soup2 = BeautifulSoup(html2, 'lxml')

    # grab url here
    image_loc = soup2.find('section', class_ = "main_feature").a['data-fancybox-href']

    #combine image location with full url
    featured_image_url = 'https://www.jpl.nasa.gov' + image_loc
    return featured_image_url

# featured_image_url = image()
# print(featured_image_url)

def FAQs():
    browser = init_browser()
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)
    tables = pd.read_html(url3)
    tables = tables[0]
    output = tables.to_html(index=False, header = None)
    return output

# tables = FAQs()
# tables

def hemispheres():
    # go to the website where the images are
    browser = init_browser()
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)
    html4 = browser.html 
    soup4 = BeautifulSoup(html4, 'lxml')

    image_list = soup4.find_all('div', class_='item')

    html_list = []

    for image in image_list:
        heading = image.h3.text
        browser.links.find_by_partial_text(heading).click()
        html5=browser.html
        soup5 = BeautifulSoup(html5, 'lxml')
        image_url = soup5.find('div', class_='downloads').a['href']
        image_url = image_url.replace("'", "")
        html_list.append({"title": heading, "img_url": image_url})
        
        browser.back()
        
    return html_list   

