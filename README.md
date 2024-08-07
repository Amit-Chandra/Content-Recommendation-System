```markdown
# Content Recommendation System using YouTube API

## Overview
This project implements a content recommendation system using the YouTube API. The system fetches video details, processes the data, and provides recommendations based on video similarity.

## Features
- Fetch video details using the YouTube API
- Preprocess video data
- Train a recommendation model
- Get video recommendations

## Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Amit-Chandra/Content-Recommendation-System.git
   cd Content-Recommendation-System
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root:
     ```
     YOUTUBE_API_KEY=your_api_key_here
     ```

## Running the Application

1. Run the data preprocessing notebook:
   ```bash
   jupyter notebook notebooks/data_preprocessing.ipynb
   ```

2. Run the model training notebook:
   ```bash
   jupyter notebook notebooks/model_training.ipynb
   ```

3. Start the Flask application:
   ```bash
   python app.py
   ```

## API Endpoints

### POST /recommend
- **Description**: Get video recommendations based on the provided video ID.
- **Request Body**:
  ```json
  {
      "video_ids": ["video_id1", "video_id2"],
      "video_id": "video_id1",
      "top_n": 5
  }
  ```
- **Response**:
  ```json
  [
      {
          "similarity_score": 0.9999970604261998,
          "title": "Video Title",
          "video_id": "video_id"
      },
      ...
  ]
  ```

## Contributing
- Contributions are welcome! Please open an issue or submit a pull request.

## License
- This project is licensed under the MIT License.
```
