import scrapy
from scrapy.crawler import CrawlerProcess
import json
from urllib.parse import urlencode
import os

class ClassCentralScraper(scrapy.Spider):
    name = "ClassCentral_scraper"

    
    def get(self):
        self.input = input("Enter a topic:")

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, utf-8",
        "Accept-Language":"en-US,en;q=0.9","Cache-Control":"max-age=0",
        "Cookie":"PHPSESSID=nt6b2uqm27s0bnldie8nbaabpv; signup_prompt=1; sessionId=be43356c642c009b7b22f3572d",
        "Referer":"https://www.classcentral.com/",
        "Sec-Ch-Ua":"\"Brave\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"\"Windows\"",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"same-origin",
        "Sec-Fetch-User":"?1",
        "Sec-Gpc":"1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    course_url = "https://www.classcentral.com/search?"
    #https://www.classcentral.com/search?q=python

    '''params = {
        "q" : "python"
    }'''

    def start_requests(self):
        search = input("Enter a topic:")
        params = {
        "q" : f"{search}"
    }
        yield scrapy.Request(
            url = self.course_url+urlencode(params),
            headers=self.headers,
            callback=self.parse
        )
    
    def ratingCalc(self,data):
        return len(data.css("i.icon-star.icon-medium"))+(len(data.css("i.icon-star-half.icon-medium"))*0.5)
    
    def print_results(self,data):
        print("Class Central results")
        for course in data:
            print("Title:",course.css("h2.text-1.weight-semi.line-tight.margin-bottom-xxsmall::text").get(),",Rating:",self.ratingCalc(course))
    
    def get_results(self,data):
        results = {}
        for ind,course in enumerate(data,len(data)):
            results[f"cc{ind}"] = {"Title":course.css("h2.text-1.weight-semi.line-tight.margin-bottom-xxsmall::text").get(),
                                  "Rating":self.ratingCalc(course)}
        return results


        
    def parse(self,response):
        print(len(response.css("li.bg-white.border-all.border-gray-light.padding-xsmall.radius-small.margin-bottom-small.medium-up-padding-horz-large.medium-up-padding-vert-medium.relative")))
        results = self.get_results(response.css("li.bg-white.border-all.border-gray-light.padding-xsmall.radius-small.margin-bottom-small.medium-up-padding-horz-large.medium-up-padding-vert-medium.course-list-course"))
        self.write_to_json_file(results)
        
    def write_to_json_file(self,data):
        f = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))+"\\FlaskApp\\courseDetails.json","r")
        jf = json.load(f)
        f.close()
        jf["ClassCentralResults"] = []
        [jf["ClassCentralResults"].append(data[course]) for course in data]
        f = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))+"\\FlaskApp\\courseDetails.json","w")
        json.dump(jf,f,indent=2)
        f.close()
        print("done")
            #file.write("Title:"+str(course.css("h2.text-1.weight-semi.line-tight.margin-bottom-xxsmall::text").get())+",Rating:"+str(self.ratingCalc(course))+"\n")

