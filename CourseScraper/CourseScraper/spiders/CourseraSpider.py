import scrapy
from scrapy.crawler import CrawlerProcess
import json
from urllib.parse import urlencode
import sys,os

class CourseraScraper(scrapy.Spider):
    name = "Coursera_scaper"

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br"
        ,"Accept-Language":"en-US,en;q=0.7",
        "Cache-Control":"max-age=0",
        "Cookie":"__204u=5213803034-1684255999853; CSRF3-Token=1695133071.kfuEVK1YPYyQ0Y7p; __204r=; __400v=6da52e09-a91e-47c8-ad4f-428900fc64e7; __EventPulseVisitId=87c3a06c-d665-404c-8f6d-f81e24d688df~1694888429609; __EventPulseInitialReferrer=https%3A%2F%2Fwww.coursera.org; post-tv-survey-in-sep-2021=true; __EventPulseLastActivityTime=1694888444653; __400vt=1694888451540",
        "Referer":"https://www.coursera.org/",
        "Sec-Ch-Ua":"\"Brave\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile":"?0","Sec-Ch-Ua-Platform":"\"Windows\"",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"same-origin",
        "Sec-Fetch-User":"?1","Sec-Gpc":"1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0"
    }

    course_url = "https://www.coursera.org/search?"
    #https://www.coursera.org/search?query=machine%20learning

    ''' params = {
        "query": f"{input}" # %20 for space
    }'''

    def start_requests(self):
        search = input("Enter a topic:")

        params = {
        "query": f"{search}" # %20 for space
        }

        yield scrapy.Request(
            url = self.course_url+urlencode(params),
            headers=self.headers,
            callback=self.parse
        )

    def print_results(self,data):
        print("Coursera Results")
        for course in data:
            print("Title:",course.css("h3.cds-119.cds-CommonCard-title.css-e7lgfl.cds-121::text").get(),",Rating:",
                                      course.css("p.cds-119.css-11uuo4b.cds-121::text").get(),"URL",course.css("a."))
            
    def get_results(self,data):
        results = {}
        for ind,course in enumerate(data,len(data)):
            results[f"c{ind}"]={"Title":course.css("h3.cds-119.cds-CommonCard-title.css-e7lgfl.cds-121::text").get(),
                                "Rating":course.css("p.cds-119.css-11uuo4b.cds-121::text").get()}
        return results

    
    
    def write_to_json_file(self,data):
        f = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))+"\\FlaskApp\\courseDetails.json","r")
        jf = json.load(f)
        f.close()
        jf["CourseraResults"] = []
        [jf["CourseraResults"].append(data[course]) for course in data]
        f = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))+"\\FlaskApp\\courseDetails.json","w")
        json.dump(jf,f,indent=2)
        f.close() 
        print("done")


    def parse(self,response):
        data = response.css("li.cds-9.css-0.cds-11.cds-grid-item.cds-56.cds-64.cds-76")
        #self.print_results(data)
        #self.write_to_file(data)
        results_json = self.get_results(data)
        self.write_to_json_file(results_json)
        yield results_json


        