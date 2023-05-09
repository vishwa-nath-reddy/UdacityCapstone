import unittest
from unittest.mock import patch, MagicMock
from app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You can access movies and venues for free', response.data)

    def test_venues(self):
        with patch('app.Venue.public') as mock_public:
            mock_venue = MagicMock()
            mock_public.return_value = mock_venue
            response = self.app.get('/venues')
            self.assertEqual(response.status_code, 200)
            mock_public.assert_called()

    def test_movies(self):
        with patch('app.Movie.public') as mock_public:
            mock_movie = MagicMock()
            mock_public.return_value = mock_movie
            response = self.app.get('/movies')
            self.assertEqual(response.status_code, 200)
            mock_public.assert_called()

    def test_show_venue(self):
        with patch('app.Show') as mock_show, \
                patch('app.Venue.public') as mock_venue, \
                patch('app.Movie.ticket_price'), \
                patch('app.Movie.name') as mock_movie_name:
            mock_show.query.filter().all.return_value = [MagicMock()]
            mock_venue.query.filter().first.return_value = MagicMock()
            mock_movie_name.filter().first.return_value = MagicMock(name='Avengers')
            response = self.app.get('/venues/1')
            self.assertEqual(response.status_code, 200)
            mock_show.query.filter().all.assert_called()
            mock_venue.query.filter().first.assert_called()
            mock_movie_name.filter().first.assert_called()

    def test_show_movie(self):
        with patch('app.Show') as mock_show, \
                patch('app.Movie.public') as mock_movie, \
                patch('app.Venue.name') as mock_venue_name, \
                patch('app.Movie.ticket_price'):
            mock_show.query.filter().all.return_value = [MagicMock()]
            mock_movie.query.filter().first.return_value = MagicMock()
            mock_venue_name.filter().first.return_value = MagicMock(name='PVR')
            response = self.app.get('/movies/1')
            self.assertEqual(response.status_code, 200)
            mock_show.query.filter().all.assert_called()
            mock_movie.query.filter().first.assert_called()
            mock_venue_name.filter().first.assert_called()

    def test_create_venue_form(self):
        with patch('app.request') as mock_request, \
                patch('app.Venue.insert') as mock_insert, \
                patch('app.jsonify') as mock_jsonify:
            mock_request.get_json.return_value = {
                'name': 'Test Venue',
                'city': 'Test City',
                'state': 'Test State',
                'address': 'Test Address',
                'capacity': 100,
                'contact_number': '1234567890'
            }
            mock_venue = MagicMock()
            mock_venue.public.return_value = {}
            mock_insert.return_value = None
            mock_jsonify.return_value = MagicMock()
            response = self.app.post('/venues/create')
            self.assertEqual(response.status_code, 200)
            mock_insert.assert_called()
            mock_venue.public.assert_called()
            mock_jsonify.assert_called()

if __name__=='__main__':
    TestApp()

