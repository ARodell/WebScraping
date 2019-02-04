# import libraries
import pandas as pd
import os
import requests
import time
from splinter import Browser
from bs4 import BeautifulSoup

# define browser
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# define where and what is scraped
def scrape():
    
    browser = init_browser()

    # create empty data dictionary for mongo
    scrape_mars = {}

    # create link to NASA mars news data url
    browser = Browser("chrome", headless=False)
    new_surl = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    mars_news_html = browser.html

    # parse data using BeatifulSoup
    mars_news_bs = BeautifulSoup(mars_news_html, "html.parser")

    div1 = mars_news_bs.find("div", class_="content_title")
    
    news_title = div1.find("a").text
    news_p = mars_news_bs.find("div", class_="article_teaser_body").text

    # add mars news title and paragraph text to scrape_mars dictionary
    scrape_mars["news_title"] = news_title
    scrape_mars["news_p"] = news_p

    # create link to JPL featured image url
    browser = Browser("chrome", headless=False)
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    browser.click_link_by_partial_text("FULL IMAGE")

    # use BeatifulSoup to parse retrieved image data
    mars_img_html = browser.html
    mars_img_bs = BeautifulSoup(mars_img_html, 'html.parser')

    nasa_home = mars_img_bs.find("article", class_="carousel_item")
    nasa_link = nasa_home.a["data-fancybox-href"]
    featured_image_url = "https://www.jpl.nasa.gov" + nasa_link

    # add featured image to scrape_mars dictionary
    scrape_mars["featured_image_url"] = featured_image_url

    # create link to Twitter account for mars weather data
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    mars_weather_html = requests.get(mars_weather_url)
    mars_weather_bs = BeautifulSoup(mars_weather_html.text, "html.parser")

    tweet = mars_weather_bs.find("div", class_="stream")
    mars_weather = tweet.find(text="Mars Weather").findNext("p").text

    # add tweets to scrape_mars dictionary
    scrape_mars["mars_weather"] = mars_weather

    # create link to url for mars facts
    mars_facts_url = "https://space-facts.com/mars/"
    mars_tables = pd.read_html(mars_facts_url)
    mars_df = mars_tables[0]
    mars_df.columns = ["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    mars_df.to_html("Mars_df.html")

    # create html script for mars facts table   
    mars_facts = mars_df.to_html()
    mars_facts.replace("\n","")
    mars_df.to_html("mars_facts.html")

    # store mars facts in scrape_mars dictionary
    scrape_mars["mars_facts"] = mars_facts

    browser = Browser("chrome", headless=False)
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    # parse data for scraped data on mars hemispheres
    mars_hemispheres_html = browser.html
    mars_hemispheres_bs = BeautifulSoup(mars_hemispheres_html, "html.parser")
    mars_images = mars_hemispheres_bs.find_all("div", class_="description")

    # create a loop to loop through each mars hemisphere image
    hemisphere_urls = []

    for image in mars_images:
        
        image_dict = {}
        
        href = image.find("h3").text
        image_dict["title"] = href
        browser.click_link_by_partial_text(href)
        
        mars_html2 = browser.html
        mars_bs2 = BeautifulSoup(mars_html2, "html.parser")
        
        url = mars_bs2.find("img", class_="wide-image")["src"]
        image_dict["img_url"] = "https://astrogeology.usgs.gov" + url
        
        hemisphere_urls.append(image_dict)
        browser.click_link_by_partial_text("Back")
        
       
    # Store hemisphere image urls to dictionary
    scrape_mars["hemisphere_urls"] = hemisphere_urls

    return scrape_mars