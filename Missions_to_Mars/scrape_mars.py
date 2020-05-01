from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/scrape")
def echo():
    return render_template("index.html", text="Mars Web-Scraping Challenge")
    

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
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    title = article.find("div", class_="content_title").text
    paragraph = article.find("div", class_ ="article_teaser_body").text
    output = [title, paragraph]
    return output


def JPLImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url


def TwitterWeather():

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    weather_soup = BeautifulSoup(html, "html.parser")
    mars_weather_tweet = weather_soup.find("div", 
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

if __name__ == "__main__":
    print(scrape)


