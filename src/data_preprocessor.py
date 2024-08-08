# src/data_preprocessor.py

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

class DataPreprocessor:
    def __init__(self, videos_df):
        self.videos_df = videos_df

    def clean_data(self):
        # Example cleaning steps: fill NaN values, drop duplicates
        self.videos_df.fillna('', inplace=True)
        self.videos_df.drop_duplicates(subset=['video_id'], inplace=True)
        return self.videos_df

    def transform_text_data(self):
        # Ensure that the 'description' column exists and is treated correctly
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


    def extract_features(self):
        # Example: include numeric features only for simplicity
        numeric_features = ['view_count', 'like_count', 'comment_count']
        feature_data = self.videos_df[numeric_features]
        return feature_data

    def save_data(self, output_path):
        """
        Save the processed data to a CSV file.
        """
        self.videos_df.to_csv(output_path, index=False)
        print(f"Processed data saved to {output_path}")








# # src/data_preprocessor.py

# from sklearn.feature_extraction.text import TfidfVectorizer
# import pandas as pd

# class DataPreprocessor:
#     def __init__(self, videos_df):
#         self.videos_df = videos_df

#     def clean_data(self):
#         """
#         Clean the video data.
#         Implement your data cleaning steps here. For example:
#         - Handling missing values
#         - Normalizing text data
#         - Converting data types
#         """
#         # Example cleaning step: dropping rows with missing values in specific columns
#         self.videos_df.dropna(subset=['title', 'description'], inplace=True)
        
#         # Add other cleaning steps as needed
#         return self.videos_df

#     def extract_features(self):
#         """
#         Extract relevant features from the video data.
#         Implement your feature extraction steps here. For example:
#         - Extracting numerical features
#         - Encoding categorical features
#         """
#         # Example: Converting tags to a string for later use in TF-IDF or other processing
#         self.videos_df['tags'] = self.videos_df['tags'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
        
#         # Add other feature extraction steps as needed
#         return self.videos_df

#     def transform_text_data(self):
#         """
#         Transform the 'description' field using TF-IDF.
#         This converts text data into a numerical format suitable for machine learning models.
#         """
#         # Create a TF-IDF Vectorizer
#         tfidf_vectorizer = TfidfVectorizer(max_features=100)

#         # Transform the text data into numerical format
#         tfidf_matrix = tfidf_vectorizer.fit_transform(self.videos_df['description'].fillna(''))

#         # Convert the sparse matrix to a DataFrame
#         tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

#         # Combine TF-IDF features with the original DataFrame
#         self.videos_df = pd.concat([self.videos_df.drop(columns=['description']), tfidf_df], axis=1)
        
#         return self.videos_df

#     def save_data(self, output_path):
#         """
#         Save the processed data to a CSV file.
#         """
#         self.videos_df.to_csv(output_path, index=False)
#         print(f"Processed data saved to {output_path}")











# # src/data_preprocessor.py

# import pandas as pd
# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.preprocessing import StandardScaler
# from datetime import datetime

# class DataPreprocessor:
#     def __init__(self, df):
#         self.df = df

#     def clean_data(self):
#         # Clean text data
#         self.df['title'] = self.df['title'].apply(self._clean_text)
#         self.df['description'] = self.df['description'].apply(self._clean_text)
#         return self.df

#     def _clean_text(self, text):
#         text = re.sub(r'http\S+', '', text)  # Remove URLs
#         text = re.sub(r'\W+', ' ', text)  # Remove special characters
#         return text.lower().strip()

#     def extract_features(self):
#         # Extract textual features using TF-IDF
#         tfidf = TfidfVectorizer(max_features=1000)
#         tfidf_matrix = tfidf.fit_transform(self.df['title'] + ' ' + self.df['description'])
#         tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf.get_feature_names_out())
        
#         # Extract duration in seconds
#         self.df['duration_seconds'] = self.df['duration'].apply(self._convert_duration)

#         # Normalize numerical features
#         scaler = StandardScaler()
#         self.df[['view_count', 'like_count', 'comment_count', 'duration_seconds']] = scaler.fit_transform(
#             self.df[['view_count', 'like_count', 'comment_count', 'duration_seconds']]
#         )
        
#         # Combine features
#         feature_data = pd.concat([self.df[['video_id', 'title']], tfidf_df], axis=1)
#         return feature_data

#     def _convert_duration(self, duration):
#         match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
#         hours = int(match.group(1)[:-1]) if match.group(1) else 0
#         minutes = int(match.group(2)[:-1]) if match.group(2) else 0
#         seconds = int(match.group(3)[:-1]) if match.group(3) else 0
#         return hours * 3600 + minutes * 60 + seconds

#     def save_data(self, output_path):
#         self.df.to_csv(output_path, index=False)







# import pandas as pd

# class DataPreprocessor:
#     def __init__(self, data):
#         self.data = data

#     def clean_data(self):
#         self.data.drop_duplicates(subset=['video_id'], inplace=True)
#         self.data.fillna('', inplace=True)
#         return self.data

#     def extract_features(self):
#         self.data['combined_text'] = self.data['title'] + ' ' + self.data['description'] + ' ' + self.data['tags'].apply(lambda x: ' '.join(x))
#         return self.data

#     def save_data(self, path):
#         self.data.to_csv(path, index=False)

# if __name__ == "__main__":
#     df = pd.read_csv('../data/videos.csv')
#     preprocessor = DataPreprocessor(df)
#     cleaned_data = preprocessor.clean_data()
#     feature_data = preprocessor.extract_features()
#     preprocessor.save_data('../data/processed_videos.csv')
