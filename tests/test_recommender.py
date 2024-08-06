import unittest
import pandas as pd
from recommender import Recommender

class TestRecommender(unittest.TestCase):
    def setUp(self):
        data = {
            'video_id': ['test1', 'test2'],
            'title': ['Title 1', 'Title 2'],
            'description': ['Description 1', 'Description 2'],
            'text': ['Title 1 Description 1', 'Title 2 Description 2']
        }
        self.df = pd.DataFrame(data)
        self.cosine_sim = pd.DataFrame([[1, 0.1], [0.1, 1]])
        self.recommender = Recommender(self.df, self.cosine_sim)

    def test_get_recommendations(self):
        recommendations = self.recommender.get_recommendations('test1', top_n=1)
        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations['video_id'].values[0], 'test2')

if __name__ == '__main__':
    unittest.main()
