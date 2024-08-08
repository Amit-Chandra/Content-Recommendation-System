
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


