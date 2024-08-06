import pandas as pd

class Recommender:
    def __init__(self, df: pd.DataFrame, cosine_sim: pd.DataFrame):
        """
        Initialize the Recommender with a DataFrame and cosine similarity matrix.
        
        :param df: DataFrame containing video data
        :param cosine_sim: Cosine similarity matrix
        """
        self.df = df
        self.cosine_sim = cosine_sim

    def get_recommendations(self, video_id: str, top_n: int = 10) -> pd.DataFrame:
        """
        Get top N recommendations for a given video ID.
        
        :param video_id: ID of the video for which recommendations are to be made
        :param top_n: Number of top recommendations to return
        :return: DataFrame containing the recommended videos
        """
        # Check if the video ID is in the DataFrame
        if video_id not in self.df['video_id'].values:
            raise ValueError("Video ID not found in the data")

        # Get index of the video that matches the video_id
        idx = self.df.index[self.df['video_id'] == video_id].tolist()[0]
        
        # Get pairwise similarity scores for the video
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort videos based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get the indices of the top N most similar videos
        sim_scores = sim_scores[1:top_n + 1]
        video_indices = [i[0] for i in sim_scores]
        
        # Return top N most similar videos
        return self.df.iloc[video_indices].reset_index(drop=True)
