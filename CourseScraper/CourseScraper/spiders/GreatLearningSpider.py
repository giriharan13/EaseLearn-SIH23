import scrapy
from scrapy.crawler import CrawlerProcess
import json
from urllib.parse import urlencode


class GreatLearningScraper(scrapy.Spider):
    name = "Great_learning_scraper"

    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, utf-8",
        "Accept-Language":"en-US,en;q=0.7",
        "Access-Control-Allow-Origin":"*",
        "Content-Type":"application/json;charset=UTF-8",
        "Cookie":"user_country_zone=in; gl_webengage=6e684859-9371-4b06-b583-1cfc0a49e808; gl_last_touch=%2Facademy; gl_first_touch=%2Facademy; glca_redirection_url_cookie=null; drift_campaign_refresh=9060a613-486b-4812-9e17-a6a5b3873de0; drift_aid=642c0386-7279-42fc-a26c-ec892f2e00e9; driftt_aid=642c0386-7279-42fc-a26c-ec892f2e00e9; careerplus_triggered=false; _gl_w3_session=J7SbUR5ThkEoqajc7jMD5BzEFG4mbsihAhtndqR2jZIMk%2F8uqiKbfxlGCTYOtwS5kpE3bFP%2BAieEAIw0AZ7lwDcl54p1iWJsZc16AAdEw2H51PihbNyYpP%2BKCDnaLb8FA779E3ZB%2F1tVsasZZhSquWEIUO6FRzH9Vzctvk5BI5Vou4KfZTfidImTSuX6zIZf1qVAcoHvQRzQ5apzjhamagkA2T8Q9gbahshk7R2pc5%2FoLad%2BA16eksSvDSvrh5dMQMpCPEm1VZjHVNvOR1UHs81vIbn056YVWjHNPUf48hiGMVF%2FQxWSO0T2idsqZpkrmXUqKqH3odDWN3Htcac9lJmKlXROHEo26FPWg94NiehL68Rh07v8JF%2Fc8iZ5G0BJrF5BUTY6d%2FL3WvoTYxo7JIC2oD5K0kzw7iIVesgHI7BDdI9ZSlEtJnx4SzHqOoFkNrlUYnnC5B70uRNdtmUstYcyMY92PF7CfxjtiwV8HWLSMq6dY%2Bhyo9PF6%2BJvFu0CNtIW%2FP8feo87KVi33S8UAoMgEVm0atRwDxj9PA2JsW%2FeX9J2v5apUM9LPVoQv3UzE1unr9pqSf%2BzVXY8ESaGHUpPNcjl2tn54sw2aS8YfjmkypNvUZxzsXa4PEanC%2Bji8Z0kDneUrk6jRlhzDryn3Zxwat3pR5napA%3D%3D--ptC%2FyM7i2bYUPm45--y7kh5YIGDWMuuwLURVt04w%3D%3D",
        "Referer":"https://www.mygreatlearning.com/academy",
        "Sec-Ch-Ua":"\"Brave\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
        "Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"\"Windows\"",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "Sec-Gpc":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36","X-Csrf-Token":"j2gdP7xhgRAdKOz+Y+VHqKEvTp+t1+fgBp+2OaH5+QttZnKiF3QYTYDoUJ7OKo0xXI6SdsDE/UqXgObpACBHvQ==",
        "X-Gl-Academy-Auth":"f3d7662b73f8c49db9f828544f73d686",
        "X-Requested-With":"XMLHttpRequest"
    }

    course_url = "https://www.mygreatlearning.com/api/v1/academy-search-data?"
    #https://www.mygreatlearning.com/api/v1/academy-search-data?company_name=learn-for-free&page_name=home_page&keyword=python

    '''params = {
        "company_name" : "learn-for-free",
        "page_name" : "home_page",
        "keyword" : f"{input}"
    }'''

    def start_requests(self):
        search = input("Enter a topic:")
        params = {
        "company_name" : "learn-for-free",
        "page_name" : "home_page",
        "keyword" : f"{search}"
    }
        
        yield scrapy.Request(
            url = self.course_url+urlencode(params),
            headers=self.headers,
            callback=self.parse
        )

    def write_to_file(self,data):
        file = open("C:\\Users\\raghu\\Documents\\testing\\CourseScrapper\\sample_output.txt","a")
        file.write("Great Learning Courses:\n")
        for course in data:
            file.write("Title:"+course["title"]+",Rating:"+str(course["course_rating"])+"\n")     



    def print_results(self,data):
        print("Great Learning Courses")
        for course in data:
            print("Title:",course["title"],",Rating:",course["course_rating"])        

        


    def parse(self,response):
        json_data = json.loads(response.text)
        self.print_results(json_data["courses"])
        self.write_to_file(json_data["courses"])


def startProcess():
    process = CrawlerProcess()
    process.crawl(GreatLearningScraper)
    process.start()
