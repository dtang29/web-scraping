import pylint
from splinter import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}

    #Scrape Latest News Title and Paragraph
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all('div', class_="image_and_description_container")
    mars_data["news_title"] = news[0].find('h3').text
    mars_data["news_p"] = news[0].find('a').text


    #Scrape Mars feature image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    jpl = soup.find_all('section', class_="centered_text clearfix main_feature primary_media_feature single")
    mars_data["featured_image_url"] = "https://www.jpl.nasa.gov/" + jpl[0].find('a', class_="button fancybox")['data-fancybox-href']

    #Scrape Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars = soup.find_all('div', class_="stream")
    mars_data["mars_weather"] = mars[0].find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #Scrape mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    df = df.rename(index=str, columns={0: "Description", 1: "Values"})
    df = df.set_index('Description')
    html_table = df.to_html()
    mars_data["html_table"] = html_table.replace('\n', '')

    #Scrape Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #Create an empty list to store the title and urls
    hemisphere_image_urls = []

    #Use BS to find the parent div class for the links to the photos
    pictures = soup.find_all('div', class_="item")
    for picture in pictures:
        
        #Grab the title of the image
        title = picture.find('h3').text
        
        #Go to the image url 
        n_url = 'https://astrogeology.usgs.gov' + picture.find('a')['href']
        browser.visit(n_url)
        n_html = browser.html
        n_soup = BeautifulSoup(n_html, 'html.parser')
        
        #Grab the url of the image
        img_url = 'https://astrogeology.usgs.gov' + n_soup.find_all('img', class_="wide-image")[0]['src']
        
        #Create empty dictionary and add each img url and title to it
        img_dict = {}
        img_dict["img_url"] = img_url
        img_dict["title"] = title
        
        #Append the dictionary to the list
        hemisphere_image_urls.append(img_dict)
        
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    
    #return our mars data dict
    return mars_data

