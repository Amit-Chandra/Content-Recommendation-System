import unittest
from unittest.mock import patch, MagicMock
from youtube_api import YouTubeAPI

class TestYouTubeAPI(unittest.TestCase):
    @patch('youtube_api.build')
    def test_get_video_details(self, mock_build):
        # Create a mock response
        mock_response = {
            'items': [{
                'id': 'test_video_id',
                'snippet': {
                    'title': 'Test Title',
                    'description': 'Test Description',
                    'tags': ['test', 'video'],
                    'categoryId': '1'
                },
                'statistics': {
                    'viewCount': '1000',
                    'likeCount': '100',
                    'commentCount': '10'
                }
            }]
        }
        mock_service = MagicMock()
        mock_service.videos().list().execute.return_value = mock_response
        mock_build.return_value = mock_service

        api = YouTubeAPI()
        video_ids = ['test_video_id']
        df = api.get_video_details(video_ids)

        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.iloc[0]['video_id'], 'test_video_id')
        self.assertEqual(df.iloc[0]['title'], 'Test Title')
        self.assertEqual(df.iloc[0]['description'], 'Test Description')

if __name__ == '__main__':
    unittest.main()
