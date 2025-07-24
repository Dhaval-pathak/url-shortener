# URL Shortener Service

## Overview
Build a simple URL shortening service similar to bit.ly or tinyurl. 



## Project Completion & Submission

### Requirements Implemented
- Shorten URL endpoint (`POST /api/shorten`)
- Redirect endpoint (`GET /<short_code>`)
- Analytics endpoint (`GET /api/stats/<short_code>`)
- In-memory, thread-safe storage
- URL validation and error handling
- 6-character alphanumeric short codes
- At least 5 comprehensive tests (see `tests/test_basic.py`)

### How to Run Tests
1. Create virtual environment
   - Windows: `pythom -m venv venv`
2. Activate your virtual environment:
   - Windows: `venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Run tests:
   - `pytest`

### Example Error Responses
- Invalid URL:
  ```json
  {"error": "Invalid URL"}
  ```
- Short code not found:
  ```json
  {"error": "Short code not found"}
  ```
- Missing URL in request body:
  ```json
  {"error": "Missing URL in request body"}
  ```

### Implementation Notes
- All data is stored in-memory and is thread-safe using `threading.Lock`.
- Each test run starts with a clean state.
- No external database or authentication is used.



