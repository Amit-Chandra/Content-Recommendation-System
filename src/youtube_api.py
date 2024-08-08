from googleapiclient.discovery import build
import os
import os
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

# Initialize the YouTube API client
def get_youtube_client():
    api_key = os.getenv('YOUTUBE_API_KEY')  # Ensure you set the YOUTUBE_API_KEY environment variable
    youtube = build('youtube', 'v3', developerKey=api_key)
    return youtube


def get_video_metadata(youtube_client, video_id):
    response = youtube_client.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    if not response['items']:
        return None

    video = response['items'][0]
    return {
        'id': video['id'],
        'title': video['snippet']['title']
    }



def compute_similarity(youtube_client, video_id1, video_id2):
    metadata1 = get_video_metadata(youtube_client, video_id1)
    metadata2 = get_video_metadata(youtube_client, video_id2)
    
    if not metadata1 or not metadata2:
        return 0

    title1 = metadata1['title']
    title2 = metadata2['title']
    
    if not title1 or not title2:
        return 0

    # Compute similarity between titles
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([title1, title2])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    
    return similarity[0][0]


def get_related_videos(youtube_client, video_id):
    # First, get the metadata of the video to use for related searches
    video_metadata = get_video_metadata(youtube_client, video_id)
    if not video_metadata:
        return []

    # Extract the title or description to use for related searches
    search_query = video_metadata['title']  # or you can use a combination of title and description

    # Perform a search to get related videos based on the query
    search_response = youtube_client.search().list(
        part='snippet',
        q=search_query,
        type='video',
        maxResults=10
    ).execute()

    recommendations = []
    for item in search_response.get('items', []):
        related_video_id = item['id']['videoId']
        similarity_score = compute_similarity(youtube_client, video_id, related_video_id)
        recommendations.append({
            'title': item['snippet']['title'],
            'video_id': related_video_id,
            'similarity_score': similarity_score
        })

    return recommendations












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


