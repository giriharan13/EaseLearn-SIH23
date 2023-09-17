import scrapy
from scrapy.crawler import CrawlerProcess
import json
from urllib.parse import urlencode

class UdemyScraper(scrapy.Spider):
    name = "Udemy_scraper"

    headers = { 
        "Accept":"application/json, text/plain, */*",
        "Accept-Encoding":"gzip, deflate, utf-8",
        "Accept-Language":"en-US",
        "Cookie":"__udmy_2_v57r=2220cb8a286b4c3ba3a5cabb1c52a19f; __udmy_1_a12z_c24t=VGhlIGFuc3dlciB0byBsaWZlLCB0aGUgdW5pdmVyc2UsIGFuZCBldmVyeXRoaW5nIGlzIDQy; ud_firstvisit=2023-09-07T13:15:53.093380+00:00:1qeErR:zgDQqu3FfPBf_DW6Pf141x-v3L8; ud_locale=en_US; ud_cache_brand=INen_US; ud_cache_marketplace_country=IN; ud_cache_price_country=IN; ud_cache_version=1; ud_cache_language=en; ud_cache_device=None; new_user=true; existing_user=true; optimizelyEndUserId=oeu1694851420395r0.5378464466458648; ud_cache_release=e4c87abf9dec0e5a1ecc; cf_clearance=.3r3FQA1SuBgicLv55aaQXl7qB1l0SUZUhUVF63qPa8-1694871618-0-1-2d756c61.b5c04974.7a743381-0.2.1694871618; __cfruid=43c311bfc8ff270e196321094ed3bacb7ca7dff3-1694877716; ud_user_jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjQ1ODg1NjAwLCJlbWFpbCI6Imxpb25raW5nMDMwNGNoYW5uZWxAZ21haWwuY29tIiwiaXNfc3VwZXJ1c2VyIjpmYWxzZSwiZ3JvdXBfaWRzIjpbXX0.qiWAYAB-GQ52qaZ_9gMm2edjqNznYF-eTPetCt0f_5o; ud_credit_unseen=0; ud_credit_last_seen=None; __udmy_4_a12z=33d7b5e075c0fe5ba1b4a59a965b935bcc76783727cb51e0dbbde46f9bb70014; csrftoken=W4P9TSDy69p0QCNSqi89318RMzq9ajKrKcvgwQJcpXDsKwNDtdxIGTfbsXFh2IZB; client_id=bd2565cb7b0c313f5e9bae44961e8db2; access_token=P143E0ygu02Rf67zst832IO5pBoqcD9rZ9A054sT; ud_last_auth_information=\"{\"backend\": \"udemy-auth\", \"suggested_user_email\": \"lionking0304channel@gmail.com\", \"suggested_user_name\": \"Giriharan\", \"suggested_user_avatar\": \"https://img-c.udemycdn.com/user/50x50/anonymous_3.png\"}:1qhX9B:JDUZMTC6WsaRO5cdyGzGNHi_hT0\"; dj_session_id=x9ki2l7ca5ck9wxus6bbbz58nbneqgbh; ud_cache_user=245885600; ud_cache_logged_in=1; ud_cache_campaign_code=NVDPRODIN35; last_searched_phrase=23eeeb4347bdd26bfc6b7ee9a3b755dd; __cf_bm=UAAFwmav0QFTY8a.C8Hw9I2WHm8qK6vsaPSfzJ75_lc-1694881158-0-AS9TwK0vKZMxp4KRkL9ORiht2+xiOs8fmm03f4NU8kWZ5ICfXWa7PcRCd45z8CefzEH9ff52zz/JBA88B9gIgAo=; ab.storage.deviceId.5cefca91-d218-4b04-8bdd-c8876ec1908d=%7B%22g%22%3A%22b7aa796d-6ea1-5d7b-8ef2-caaf1cf47ff9%22%2C%22c%22%3A1678157457925%2C%22l%22%3A1694881164707%7D; ab.storage.userId.5cefca91-d218-4b04-8bdd-c8876ec1908d=%7B%22g%22%3A%22245885600%22%2C%22c%22%3A1694877840698%2C%22l%22%3A1694881164707%7D; query_session_identifier_id=ZDNhMDA3YmMtYTAzMS00MW; OptanonConsent=isGpcEnabled=1&datestamp=Sat+Sep+16+2023+21%3A54%3A51+GMT%2B0530+(India+Standard+Time)&version=202305.1.0&browserGpcFlag=1&isIABGlobal=false&hosts=&consentId=14f21482-5ea3-4fad-bd64-7175b80a7913&interactionCount=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0005%3A0%2CC0004%3A0%2CC0001%3A1%2CC0002%3A1&AwaitingReconsent=false; ab.storage.sessionId.5cefca91-d218-4b04-8bdd-c8876ec1908d=%7B%22g%22%3A%22b70681cd-280f-041f-cb3b-eea8d625b66a%22%2C%22e%22%3A1694883294152%2C%22c%22%3A1694881164706%2C%22l%22%3A1694881494152%7D; evi=\"3@dwRHuySxwrrK6hwVaOWeDzsl8Zya4Y1ou3xI1XwTwLBJrJOPWsUGXCCr4NNAFcYQsTa_ICJ5mAU5ylRzkScR-Eay0MrXGa7w5-0=\"; ud_rule_vars=eJxljtFqAyEQRX9l8bXNMo66u863LMho3FaaIlE3LyH_XiEJpATu03DPnHsVjctXbPHoLqmmlgshIgS_MC6T10F5VmwCey-DQZZ2o5DzT4qCBnFdxZZKbXfWHbnFtd9XgYDqAD3zAEgGSNsRF2X1_AFAAKv47K0Td7TlPXy7VnjbUnA17yVEd-GS2J8e32rML0DolRofypZ-_yntQU6DBFIzSRzR2kWaN2WJ5z3W9713eCI0BDgqraWEJ3wTtz8EzVj8:1qhY6Q:K_XorCoQ98lDpyZ8QqsOrPeOfe8; eventing_session_id=FZPIw_B8RFG3oi1QpcD_mg-1694883301552",
        "Referer":f"https://www.udemy.com/courses/search/?src=ukw&q={input}",
        "Sec-Ch-Ua":"\"Brave\";v=\"117\",\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\""
        ,"Sec-Ch-Ua-Mobile":"?0",
        "Sec-Ch-Ua-Platform":"\"Windows\"",
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "Sec-Gpc":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "X-Requested-With":"XMLHttpRequest",
        "X-Udemy-Cache-Brand":"INen_US",
        "X-Udemy-Cache-Campaign-Code":"NVDPRODIN35",
        "X-Udemy-Cache-Device":"None",
        "X-Udemy-Cache-Language":"en",
        "X-Udemy-Cache-Logged-In":"1",
        "X-Udemy-Cache-Marketplace-Country":"IN",
        "X-Udemy-Cache-Price-Country":"IN",
        "X-Udemy-Cache-Release":"e4c87abf9dec0e5a1ecc",
        "X-Udemy-Cache-User":"245885600",
        "X-Udemy-Cache-Version":"171"
        }
    
    course_url = "https://www.udemy.com/api-2.0/search-courses/?"
    # https://www.udemy.com/api-2.0/search-courses/?src=ukw&q=python&skip_price=true

    '''params = {
        "src" : "ukw",
        "q" : f"{input}",
        "skip_price" : "true"
    }'''

    def start_requests(self):
        
        search = input("Enter a topic:")
        self.headers["Referer"]=f"https://www.udemy.com/courses/search/?src=ukw&q={search}",

        params = {
        "src" : "ukw",
        "q" : f"{search}",
        "skip_price" : "true"
    }
        yield scrapy.Request(
            url = self.course_url+urlencode(params),
            headers=self.headers,
            callback=self.parse
        )

    def print_results(self,data):
        print("Udemy Courses")
        for course in data:
            print("Title:",course["title"],",Rating:",course["rating"])

    def write_to_file(self,data):
        file = open("C:\\Users\\raghu\\Documents\\testing\\CourseScrapper\\sample_output.txt","a")
        file.write("Udemy Courses:\n")
        for course in data:
            file.write("Title:"+course["title"]+",Rating:"+str(course["rating"])+"\n")


    def parse(self,response):

        #response_body_string = io.BytesIO(response.body).read().decode('br')
        #response_body_string = re.sub(r'\\x..', lambda m: chr(int(m.group(1), 16)), response_body_string)
        json_data = json.loads(response.text)["courses"]
        self.print_results(json_data)
        self.write_to_file(json_data)
        #print(json.dumps(json_data[0],indent=2))



def startProcess():
    process = CrawlerProcess()
    process.crawl(UdemyScraper)
    process.start()