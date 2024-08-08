import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class Recommender:
    def __init__(self, videos_df):
        self.videos_df = videos_df
        self.similarity_matrix = None

    def transform_text_data(self):
        if 'description' in self.videos_df.columns:
            # Handle any missing values or non-string data
            self.videos_df['description'] = self.videos_df['description'].fillna('')

            # Create a TF-IDF Vectorizer
            tfidf_vectorizer = TfidfVectorizer(max_features=100)
            
            # Transform the text data into numerical format
            tfidf_matrix = tfidf_vectorizer.fit_transform(self.videos_df['description'])
            
            # Convert the sparse matrix to a DataFrame
            tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
            
            # Combine TF-IDF features with the original DataFrame
            self.videos_df = pd.concat([self.videos_df.drop(columns=['description']), tfidf_df], axis=1)
        else:
            raise KeyError("Column 'description' not found in DataFrame")
        
        return self.videos_df

    def train_model(self):
        # Ensure DataFrame is available and has columns
        if hasattr(self, 'videos_df'):
            print("Columns in DataFrame:")
            print(self.videos_df.columns)
        else:
            print("DataFrame is not defined.")
        
        # Ensure features are numeric
        features = self.videos_df.drop(columns=['video_id', 'title', 'description', 'tags'], errors='ignore')
        
        # Ensure all columns are numeric
        assert features.applymap(lambda x: isinstance(x, (int, float))).all().all(), "Non-numeric data found in features matrix."
        
        # Print data types and sample data
        print("Data Types of Features:")
        print(features.dtypes)

        print("\nSample Data of Features:")
        print(features.head())
        
        # Compute cosine similarity
        self.similarity_matrix = cosine_similarity(features)


    def get_recommendations(self, video_id):
        if not hasattr(self, 'videos_df'):
            print("The 'videos_df' attribute is missing.")
            return None

        print(f"Available video IDs: {self.videos_df['video_id'].values}")

        if video_id not in self.videos_df['video_id'].values:
            print(f"Video ID '{video_id}' not found in the DataFrame.")
            return None

        video_idx = self.videos_df.index[self.videos_df['video_id'] == video_id].tolist()[0]
        print(f"Index of video ID '{video_id}': {video_idx}")

        similarity_scores = list(enumerate(self.similarity_matrix[video_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = similarity_scores[1:11]

        video_indices = [i[0] for i in similarity_scores]
        print(f"Recommended video indices: {video_indices}")

        recommendations = self.videos_df.iloc[video_indices]

        return recommendations

