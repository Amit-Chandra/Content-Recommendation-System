import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, df):
        self.df = df
        self.similarity_matrix = None

    def train_model(self):
        # Assuming feature_data is a DataFrame with necessary features for recommendation
        feature_data = self.df[['view_count', 'like_count', 'comment_count']]  # Example features
        self.similarity_matrix = cosine_similarity(feature_data)

    def get_recommendations(self, video_id, top_n=5):
        # Find the index of the video_id in the DataFrame
        video_idx = self.df.index[self.df['video_id'] == video_id].tolist()
        if not video_idx:
            return []
        
        video_idx = video_idx[0]
        similarity_scores = list(enumerate(self.similarity_matrix[video_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[1:top_n+1]  # Exclude the video itself
        
        recommended_videos = []
        for idx, score in similarity_scores:
            recommended_videos.append({
                'video_id': self.df.iloc[idx]['video_id'],
                'title': self.df.iloc[idx]['title'],
                'similarity_score': score
            })
        
        return recommended_videos

    def update_data(self, new_data):
        # Append new data to the existing DataFrame
        self.df = pd.concat([self.df, new_data], ignore_index=True)
        self.train_model()  # Retrain the model with the updated data
