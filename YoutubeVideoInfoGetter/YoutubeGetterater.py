from googleapiclient.discovery import build
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class YoutubeVideoInfoGetterater:  # Getter + Rater -> Getterater ;) ok i'll stop
    api_key = os.getenv("API_KEY")  # Set up the YouTube Data API client
    youtube = build('youtube', 'v3', developerKey=api_key)

    #Make sure to pass the topic during instantiation
    def __init__(self,topic):
        self.topic = topic

    #function for resetting the topic
    def reset_topic(self,topic):
        self.topic = topic

    #this function searches for videos
    def search(self):
        search_response = self.youtube.search().list(
            q=self.topic,
            type='video',
            maxResults=50,
            part='snippet'
        ).execute()
        return search_response
    

        #this function extracts the video data from the search response
    def extract_video_data(self,search_response):
        video_data = []
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                video_id = search_result['id']['videoId']
                title = search_result['snippet']['title']
                published_at = search_result['snippet']['publishedAt']
                channel_title = search_result["snippet"]["channelTitle"]
                video_data.append([video_id, title, published_at,channel_title])
        return video_data
    
    def standardize(self,video_ratings):
        mean = np.mean(video_ratings)
        std_dev = np.std(video_ratings)
        for i in range(len(video_ratings)):
            video_ratings[i] = (video_ratings[i]-mean)/std_dev
        return video_ratings


#this function calculates and stores video ratings based on the ratio of views,likes and comments
    def rate(self,video_data):
        video_ratings = []
        for video in video_data:
            try:
                video_stats = self.youtube.videos().list(
                    part="statistics",
                    id=video[0]
                ).execute()

                view_count = int(video_stats['items'][0]['statistics']['viewCount'])
                like_count = int(video_stats['items'][0]['statistics']['likeCount'])
              #  comment_count = int(video_stats['items'][0]['statistics']['commentCount'])
                comment_count = 0
                # Calculate the ratio of views to likes, you can use any ratio logic you prefer
                ratio = view_count / (like_count + 1)  # Add 1 to prevent division by zero

                # Use a custom rating logic based on the ratio (you can adjust this as needed)
                #rating = min(5, max(1, int(5 * ratio)))
                rating = (((like_count/ view_count) **0.5) + ((comment_count/view_count)**0.5) + ((view_count / 100000) **0.5))

                video_ratings.append(rating)
            except Exception as e:
                print(f"Error fetching video statistics: {e}")
                video_ratings.append(0)  # Assign a default rating of 0 in case of an error
        #Standardizing the video_ratings
        video_ratings = self.standardize(video_ratings)
        return video_ratings
    
    def get_results(self):
        search_response =  self.search()
        video_data = self.extract_video_data(search_response)
        video_ratings = self.rate(video_data)

        # Combine video data with ratings
        videos_with_ratings = [(video_data[i], video_ratings[i]) for i in range(len(video_data))]

        # Sort the videos based on ratings in descending order
        videos_with_ratings.sort(key=lambda x: x[1], reverse=True)

        # Display the top 50 videos with the highest ratings
        top_50_videos = videos_with_ratings[:50]
        return top_50_videos
    
    def print_results(self,videos_with_rating):
        for i, (video, rating) in enumerate(videos_with_rating, start=1):
            video_id, title, published_at,channel_title = video

            print(f"Video {i}:")
            print(f"  Channel name: {channel_title}")
            print(f"  Video ID: {video_id}")
            print(f"  Title: {title}")
            print(f"  Published At: {published_at}")
            print(f"  Rating: {rating}\n")
