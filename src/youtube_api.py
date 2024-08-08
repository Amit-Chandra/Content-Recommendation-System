from googleapiclient.discovery import build
import os
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the YouTube API client
def get_youtube_client():
    api_key = os.getenv('YOUTUBE_API_KEY')  # Ensure you set the YOUTUBE_API_KEY environment variable
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube

def get_related_videos(youtube, video_id):
    try:
        # Fetch the video details to get its category (if needed)
        video_response = youtube.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        if 'items' not in video_response or not video_response['items']:
            return []

        # Example: using video title to search related videos
        video_title = video_response['items'][0]['snippet']['title']

        response = youtube.search().list(
            part='snippet',
            q=video_title,  # Searching with the video title
            type='video',
            maxResults=10
        ).execute()

        videos = response.get('items', [])
        recommendations = []

        for video in videos:
            video_data = {
                'video_id': video['id']['videoId'],
                'title': video['snippet']['title'],
                'description': video['snippet']['description'],
                'thumbnail': video['snippet']['thumbnails']['default']['url']
            }
            recommendations.append(video_data)

        return recommendations
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


















# from googleapiclient.discovery import build
# import pandas as pd
# import os
# from dotenv import load_dotenv

# load_dotenv()

# class YouTubeAPI:
#     def __init__(self):
#         self.api_key = os.getenv('YOUTUBE_API_KEY')
#         self.youtube = build('youtube', 'v3', developerKey=self.api_key)

#     def get_video_details(self, video_ids):
#         response = self.youtube.videos().list(
#             part="snippet,contentDetails,statistics",
#             id=','.join(video_ids)
#         ).execute()

#         videos = []
#         for item in response['items']:
#             video_data = {
#                 'video_id': item['id'],
#                 'title': item['snippet']['title'],
#                 'description': item['snippet']['description'],
#                 'tags': item['snippet'].get('tags', []),
#                 'category_id': item['snippet']['categoryId'],
#                 'view_count': int(item['statistics']['viewCount']),
#                 'like_count': int(item['statistics'].get('likeCount', 0)),
#                 'comment_count': int(item['statistics'].get('commentCount', 0))
#             }
#             videos.append(video_data)
        
#         return pd.DataFrame(videos)


