from flask import Flask, request, render_template
from src.youtube_api import get_youtube_client, get_related_videos  # Adjust the path according to your structure

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_id = request.form.get('video_id')  # Get the video ID from the form
        if video_id:
            return redirect(url_for('recommend', video_id=video_id))
    return render_template('index.html')

# @app.route('/recommend')
# def recommend():
#     video_id = request.args.get('video_id')  # Get the video ID from the query parameters
#     if not video_id:
#         return redirect(url_for('index'))  # Redirect to index if no video ID is provided

#     youtube = get_youtube_client()
#     youtube_recommendations = get_related_videos(youtube, video_id)

#     return render_template('index.html', recommendations=youtube_recommendations)

@app.route('/recommend')
def recommend():
    video_id = request.args.get('video_id')
    youtube_client = get_youtube_client()
    youtube_recommendations = get_related_videos(youtube_client, video_id)
    
    # Add a default similarity_score if it's not present
    for rec in youtube_recommendations:
        if 'similarity_score' not in rec or rec['similarity_score'] is None:
            rec['similarity_score'] = 0  # or any other default value
    
    return render_template('index.html', recommendations=youtube_recommendations)

if __name__ == '__main__':
    app.run(debug=True)

