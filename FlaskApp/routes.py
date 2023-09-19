import os 
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.dirname(current_dir))

from CourseScrapper.CourseScrapper.spiders import UdemySpider,ClassCentralSpider,CourseraSpider,GreatLearningSpider
from YoutubeVideoInfoGetter.YoutubeGetterater import YoutubeVideoInfoGetterater
from WebsiteScrater.WebsiteScrater import WebsiteScrater

# add the routes here