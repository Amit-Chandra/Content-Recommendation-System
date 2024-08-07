from flask import Flask, request, jsonify, render_template
import pandas as pd
from src.recommender import Recommender
from src.youtube_api import YouTubeAPI
from src.data_preprocessor import DataPreprocessor
from utils.helpers import get_top_recommendations
import os
import sys

app = Flask(__name__)

project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

data_path = 'data/processed_videos.csv'
df = pd.read_csv(data_path)

recommender = Recommender(df)
recommender.train_model()

def remove_duplicates(recommendations):
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec['video_id'] not in seen:
            seen.add(rec['video_id'])
            unique_recommendations.append(rec)
    return unique_recommendations

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    video_ids = data['video_ids']
    video_id = data['video_id']
    top_n = data.get('top_n', 5)
    
    yt_api = YouTubeAPI()
    videos_df = yt_api.get_video_details(video_ids)
    
    preprocessor = DataPreprocessor(videos_df)
    cleaned_data = preprocessor.clean_data()
    feature_data = preprocessor.extract_features()

    recommender.update_data(feature_data)
    
    recommendations = recommender.get_recommendations(video_id, top_n)
    
    recommendations = remove_duplicates(recommendations)
    
    top_recommendations = get_top_recommendations(recommendations, top_n)
    
    return jsonify(top_recommendations)

if __name__ == '__main__':
    app.run(debug=True)















