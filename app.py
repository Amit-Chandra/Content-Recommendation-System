from flask import Flask, request, render_template, jsonify
from youtube_api import YouTubeAPI
from data_preprocessor import DataPreprocessor
from recommender import Recommender
from urllib.parse import urlparse, parse_qs


app = Flask(__name__)

# Initialize API and Data Processor
api = YouTubeAPI()
default_video_ids = ['DSq1pfn_CR0']  # Example video ID
df = api.get_video_details(default_video_ids)
data_preprocessor = DataPreprocessor(df)
df = data_preprocessor.preprocess()
cosine_sim = data_preprocessor.compute_similarity()
recommender = Recommender(df, cosine_sim)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    video_id = request.args.get('video_id')  # Get video ID from query parameter
    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    try:
        recommendations = recommender.get_recommendations(video_id)
        return jsonify(recommendations.to_dict(orient='records'))
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True)






















# app = Flask(__name__)

# def extract_video_id(url):
#     parsed_url = urlparse(url)
#     query_params = parse_qs(parsed_url.query)
#     return query_params.get('v', [None])[0]

# # Initialize API and Data Processor
# api = YouTubeAPI()
# default_video_ids = ['DSq1pfn_CR0']  # Example video ID
# df = api.get_video_details(default_video_ids)
# data_preprocessor = DataPreprocessor(df)
# df = data_preprocessor.preprocess()
# cosine_sim = data_preprocessor.compute_similarity()
# recommender = Recommender(df, cosine_sim)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/recommend', methods=['GET'])
# def recommend():
#     url = request.args.get('video_id')  # Get full URL from query parameter
#     if not url:
#         return jsonify({'error': 'URL is required'}), 400

#     video_id = extract_video_id(url)  # Extract video ID from the URL
#     if not video_id:
#         return jsonify({'error': 'Invalid YouTube URL'}), 400

#     try:
#         recommendations = recommender.get_recommendations(video_id)
#         return jsonify(recommendations.to_dict(orient='records'))
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
































# from flask import Flask, request, render_template, jsonify
# from youtube_api import YouTubeAPI
# from data_preprocessor import DataPreprocessor
# from recommender import Recommender

# app = Flask(__name__)

# # Initialize API and Data Processor
# api = YouTubeAPI()
# default_video_ids = ['dQw4w9WgXcQ']  # Example video ID
# df = api.get_video_details(default_video_ids)
# print(df.columns)  # Print columns to debug

# data_preprocessor = DataPreprocessor(df)
# df = data_preprocessor.preprocess()
# cosine_sim = data_preprocessor.compute_similarity()  # Ensure method exists
# recommender = Recommender(df, cosine_sim)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/recommend', methods=['GET'])
# def recommend():
#     video_id = request.args.get('video_id')
#     if not video_id:
#         return jsonify({'error': 'Video ID is required'}), 400

#     try:
#         recommendations = recommender.get_recommendations(video_id)
#         return jsonify(recommendations.to_dict(orient='records'))
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 404

# if __name__ == '__main__':
#     app.run(debug=True)
