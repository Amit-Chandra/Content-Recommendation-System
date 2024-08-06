import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DataPreprocessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.tfidf_matrix = None
        self.cosine_sim = None

    def preprocess(self) -> pd.DataFrame:
        if 'title' not in self.df.columns or 'description' not in self.df.columns:
            raise KeyError("Expected columns are missing from the DataFrame")

        self.df['text'] = self.df['title'] + ' ' + self.df['description']
        return self.df

    def compute_similarity(self) -> pd.DataFrame:
        # Ensure the 'text' column is present
        if 'text' not in self.df.columns:
            raise KeyError("Text column is missing from the DataFrame")

        # Compute TF-IDF matrix
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.df['text'])
        
        # Compute cosine similarity
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        return self.cosine_sim
