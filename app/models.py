import threading
from datetime import datetime

# In-memory storage for URL mappings
url_store = {}
# Structure: { short_code: { 'url': ..., 'created_at': ..., 'clicks': ... } }

# Lock for thread safety
store_lock = threading.Lock()


def save_url_mapping(short_code, url):
    with store_lock:
        url_store[short_code] = {
            'url': url,
            'created_at': datetime.utcnow().isoformat(),
            'clicks': 0
        }


def get_url_mapping(short_code):
    with store_lock:
        return url_store.get(short_code)


def increment_click(short_code):
    with store_lock:
        if short_code in url_store:
            url_store[short_code]['clicks'] += 1
            return True
        return False


def get_stats(short_code):
    with store_lock:
        data = url_store.get(short_code)
        if data:
            return {
                'url': data['url'],
                'clicks': data['clicks'],
                'created_at': data['created_at']
            }
        return None