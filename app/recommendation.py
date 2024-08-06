import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

def preprocess_data(video_df):
    video_df['description'].fillna('', inplace=True)
    video_df['text'] = video_df['title'] + ' ' + video_df['description'] + ' ' + video_df['tags'].apply(lambda x: ' '.join(x))
    
    tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = tfidf.fit_transform(video_df['text'])
    
    scaler = MinMaxScaler()
    video_df[['view_count', 'like_count', 'comment_count']] = scaler.fit_transform(video_df[['view_count', 'like_count', 'comment_count']])
    
    return video_df, tfidf_matrix

# def train_collaborative_filtering(user_item_df):
#     interaction_matrix = user_item_df.pivot(index='user_id', columns='video_id', values='interaction').fillna(0)
#     print("Interaction matrix shape:", interaction_matrix.shape)
#     interaction_sparse_matrix = csr_matrix(interaction_matrix)
    
#     n_components = min(50, interaction_sparse_matrix.shape[1])
#     print(f"Using n_components: {n_components}")  # Debugging output
#     svd = TruncatedSVD(n_components=n_components, random_state=42)
#     user_factors = svd.fit_transform(interaction_sparse_matrix)
#     item_factors = svd.components_.T
    
#     return user_factors, item_factors

def train_collaborative_filtering(user_item_df):
    interaction_matrix = user_item_df.pivot(index='user_id', columns='video_id', values='interaction').fillna(0)
    print("Interaction matrix shape:", interaction_matrix.shape)
    interaction_sparse_matrix = csr_matrix(interaction_matrix)
    
    n_components = min(50, interaction_sparse_matrix.shape[1])
    print(f"Using n_components: {n_components}")  # Debugging output
    svd = TruncatedSVD(n_components=n_components, random_state=42)
    user_factors = svd.fit_transform(interaction_sparse_matrix)
    item_factors = svd.components_.T
    
    return user_factors, item_factors





def get_content_recommendations(video_id, similarity_matrix, video_df, top_n=10):
    idx = video_df[video_df['video_id'] == video_id].index[0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    
    video_indices = [i[0] for i in sim_scores]
    return video_df.iloc[video_indices]

def get_hybrid_recommendations(user_id, user_factors, item_factors, content_similarity, video_df, user_item_df, top_n=10):
    user_idx = user_item_df['user_id'].unique().tolist().index(user_id)
    cf_scores = np.dot(user_factors[user_idx], item_factors.T)
    
    top_cf_indices = cf_scores.argsort()[-top_n:][::-1]
    top_cf_videos = video_df.iloc[top_cf_indices]
    
    hybrid_recommendations = []
    for video_id in top_cf_videos['video_id']:
        content_recs = get_content_recommendations(video_id, content_similarity, video_df, top_n=1)
        hybrid_recommendations.append(content_recs)
    
    hybrid_recommendations_df = pd.concat(hybrid_recommendations).drop_duplicates().head(top_n)
    return hybrid_recommendations_df
