import unittest
from flask import Flask
from app import app  # Import the Flask app

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_recommendation(self):
        # Send a request to the /recommend endpoint
        response = self.app.get('/recommend?video_id=test_video_id')
        self.assertEqual(response.status_code, 200)
        data = response.json
        self.assertTrue(len(data) > 0)
        self.assertIn('title', data[0])
        self.assertIn('view_count', data[0])

if __name__ == '__main__':
    unittest.main()
