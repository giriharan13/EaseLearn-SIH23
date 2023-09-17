from scrapy.crawler import CrawlerProcess
from CourseScrapper.spiders.UdemySpider import UdemyScraper
from CourseScrapper.spiders.CourseraSpider import CourseraScraper
from CourseScrapper.spiders.GreatLearningSpider import GreatLearningScraper
from CourseScrapper.spiders.ClassCentralSpider import ClassCentralScraper


if __name__=="__main__":
    
    process = CrawlerProcess()
    process.crawl(UdemyScraper)
    process.crawl(CourseraScraper)
    process.crawl(GreatLearningScraper)
    process.crawl(ClassCentralScraper)
    process.start()
