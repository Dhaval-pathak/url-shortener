import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_url_success(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data


def test_shorten_url_invalid(client):
    response = client.post('/api/shorten', json={'url': 'not-a-url'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data


def test_redirect_and_click_count(client):
    # Shorten a URL
    response = client.post('/api/shorten', json={'url': 'https://example.com/page'})
    short_code = response.get_json()['short_code']
    # Redirect
    response = client.get(f'/{short_code}', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://example.com/page'
    # Check click count
    stats = client.get(f'/api/stats/{short_code}').get_json()
    assert stats['clicks'] == 1


def test_redirect_not_found(client):
    response = client.get('/abcdef', follow_redirects=False)
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data


def test_stats_not_found(client):
    response = client.get('/api/stats/abcdef')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data