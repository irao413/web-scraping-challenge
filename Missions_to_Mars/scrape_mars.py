from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


executable_path = {'executable_path': 'C:/Users/astro/Downloads/chromedriver.exe'}
browser = Browser('chrome', **executable_path)

def scrape():
    data = {}
    output = marsNews()
    data["mars_news"] = output[0]
    data["mars_paragraph"] = output[1]
    data["JPL_image"] = JPLImage()
    data["Twitter_weather"] = TwitterWeather()
    data["mars_facts"] = marsFacts()

    return data

def marsNews():
    url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    news = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    title = article.find("div", class_="content_title").text
    paragraph = article.find("div", class_ ="article_teaser_body").text
    output = [title, paragraph]
    return output


def JPLImage():
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    JPL = BeautifulSoup(html, "html.parser")
    image = JPL.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


def TwitterWeather():

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_tweet = BeautifulSoup(html, "html.parser")
    mars_weather_tweet = weather_tweet.find("div", 
                                       attrs={
                                           "class": "tweet", 
                                            "data-name": "Mars Weather"
                                        })
    mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    return mars_weather

def marsFacts():
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    mars_df = pd.read_html(facts_url)[0]
    mars_df.columns = ["Description", "Data"]
    mars_df = mars_df.set_index("Description")
    mars_facts = mars_df.to_html(index = True, header =True)
    return mars_facts





