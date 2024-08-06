from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class YouTubeAPI:
    def __init__(self):
        # Read API key from environment variable
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def get_video_details(self, video_ids):
        response = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(video_ids)
        ).execute()

        videos = []
        for item in response['items']:
            video_data = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'tags': item['snippet'].get('tags', []),
                'category_id': item['snippet']['categoryId'],
                'view_count': int(item['statistics']['viewCount']),
                'like_count': int(item['statistics'].get('likeCount', 0)),
                'comment_count': int(item['statistics'].get('commentCount', 0))
            }
            videos.append(video_data)
        
        return pd.DataFrame(videos)

# Usage example:
# Initialize API without passing the key directly
# api = YouTubeAPI()
# video_ids = ['Ks-_Mh1QhMc', 'dQw4w9WgXcQ']
# video_df = api.get_video_details(video_ids)
# print(video_df.head())
