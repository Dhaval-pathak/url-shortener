from flask import Flask, jsonify, request, redirect
from app.models import save_url_mapping, get_url_mapping, increment_click, get_stats
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL in request body'}), 400
    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({'error': 'Invalid URL'}), 400
    # Generate a unique short code
    for _ in range(5):  # Try up to 5 times to avoid collision
        short_code = generate_short_code()
        if not get_url_mapping(short_code):
            break
    else:
        return jsonify({'error': 'Could not generate unique short code'}), 500
    save_url_mapping(short_code, long_url)
    short_url = request.host_url.rstrip('/') + '/' + short_code
    return jsonify({'short_code': short_code, 'short_url': short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    mapping = get_url_mapping(short_code)
    if not mapping:
        return jsonify({'error': 'Short code not found'}), 404
    increment_click(short_code)
    return redirect(mapping['url'], code=302)

@app.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    stats = get_stats(short_code)
    if not stats:
        return jsonify({'error': 'Short code not found'}), 404
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)