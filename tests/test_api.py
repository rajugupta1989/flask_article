import unittest
import json
from run import app
from extensions import db
from api.models import Article, Comment

class TestArticleAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_articles(self):
        response = self.client.get('/api/articles')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue('data' in data)
        self.assertTrue(isinstance(data['data'], list))

    def test_create_article(self):
        article_data = {
            'title': 'Test Article',
            'content': 'This is a test article.',
            'author': 'Test Author'
        }
        response = self.client.post('/api/articles', json=article_data)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue('data' in data)
        self.assertEqual(data['data']['title'], article_data['title'])

    def test_get_articles_sorted(self):
        # Create multiple articles
        self.client.post('/api/articles', json={
            'title': 'Article C',
            'content': 'Content C',
            'author': 'Author A'
        })
        self.client.post('/api/articles', json={
            'title': 'Article A',
            'content': 'Content A',
            'author': 'Author B'
        })
        self.client.post('/api/articles', json={
            'title': 'Article B',
            'content': 'Content B',
            'author': 'Author C'
        })

        # Test ascending sort by title
        response = self.client.get('/api/articles?sort_by=title&sort_order=asc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        titles = [article['title'] for article in data['data']]
        self.assertEqual(titles, ['Article A', 'Article B', 'Article C'])

        # Test descending sort by author
        response = self.client.get('/api/articles?sort_by=author&sort_order=desc')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        authors = [article['author'] for article in data['data']]
        self.assertEqual(authors, ['Author C', 'Author B', 'Author A'])

    # Add more test cases for other endpoints (GET specific article, POST comment, PUT article, DELETE article)

if __name__ == '__main__':
    unittest.main()
