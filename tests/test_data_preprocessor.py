import unittest
import pandas as pd
from data_preprocessor import DataPreprocessor

class TestDataPreprocessor(unittest.TestCase):
    def setUp(self):
        self.data = {
            'video_id': ['test1', 'test2'],
            'title': ['Title 1', 'Title 2'],
            'description': ['Description 1', 'Description 2']
        }
        self.df = pd.DataFrame(self.data)
        self.preprocessor = DataPreprocessor(self.df)

    def test_preprocess(self):
        processed_df = self.preprocessor.preprocess()
        self.assertIn('text', processed_df.columns)
        self.assertEqual(processed_df['text'][0], 'Title 1 Description 1')

    def test_compute_similarity(self):
        self.preprocessor.preprocess()
        cosine_sim = self.preprocessor.compute_similarity()
        self.assertEqual(cosine_sim.shape, (2, 2))

if __name__ == '__main__':
    unittest.main()
