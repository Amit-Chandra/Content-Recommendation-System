# src/data_preprocessor.py
import pandas as pd

class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def clean_data(self):
        # Remove duplicates
        self.data.drop_duplicates(subset=['video_id'], inplace=True)
        # Fill missing values if any
        self.data.fillna('', inplace=True)
        return self.data

    def extract_features(self):
        # Combine relevant text fields for text-based features
        self.data['combined_text'] = self.data['title'] + ' ' + self.data['description'] + ' ' + self.data['tags'].apply(lambda x: ' '.join(x))
        return self.data

    def save_data(self, path):
        self.data.to_csv(path, index=False)

# Example usage
if __name__ == "__main__":
    df = pd.read_csv('../data/videos.csv')
    preprocessor = DataPreprocessor(df)
    cleaned_data = preprocessor.clean_data()
    feature_data = preprocessor.extract_features()
    preprocessor.save_data('../data/processed_videos.csv')
