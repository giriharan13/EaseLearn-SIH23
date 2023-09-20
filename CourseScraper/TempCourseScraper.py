import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

class CourseScraper:
    
    def __init__(self,topic):
        self.topic = topic

    def reset_topic(self,topic):
        self.topic = topic
    
    def scrape_coursera(self):
        params = {
        "query": self.topic.replace(" ","%20") # %20 for space
        }
        url = "https://www.coursera.org/search?"+urlencode(params)
        req = requests.get(url)
        soup = BeautifulSoup(req.text,"lxml")
        courses = soup.find_all("li" ,{"class":"cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76"})

        results = {"courses":[]}
        for course in courses:
            results["courses"].append({"title":course.find("h3",
                                                        {"class":"cds-119 cds-CommonCard-title css-e7lgfl cds-121"}).text,
                                "rating":course.find("p",{"class":"cds-119 css-11uuo4b cds-121"}).text,"url":"www.coursera.org"+str(course.find("a")["href"])})
        return results
