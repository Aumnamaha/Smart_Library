# Smart Library API Documentation

Complete API reference for the Smart Library application.

---

## Base URL

```
http://127.0.0.1:8000/api/v1
```

---

## Health Check

### GET /health

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-07-20T10:30:00"
}
```

---

## Voice Recording Endpoints

### Start Recording Session

**POST** `/voice/record`

Start a new voice recording session.

**Request Body:**
```json
{
  "max_duration": 60,
  "format": "wav"
}
```

**Response:**
```json
{
  "session_id": "abc12345",
  "status": "recording",
  "max_duration_seconds": 60,
  "message": "Recording started. Speak your book query."
}
```

---

### Stop Recording & Transcribe

**POST** `/voice/stop/{session_id}`

Stop recording and transcribe the audio to text.

**Request Body:** (Optional)
```json
{
  "continue_search": true
}
```

**Response:**
```json
{
  "session_id": "abc12345",
  "transcript": "I want to read Wings of Fire by apj kalam",
  "status": "completed",
  "next_step": "query will be parsed automatically"
}
```

---

### Get Transcript

**GET** `/voice/transcript/{session_id}`

Retrieve the transcription result.

**Response:**
```json
{
  "session_id": "abc12345",
  "transcript": "I want to read Wings of Fire by apj kalam",
  "confidence": 0.95
}
```

---

## Book Search Endpoints

### Search for Books

**GET** `/books/search` or **POST** `/books/search`

Search for books across multiple open source platforms.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | No | Book title to search |
| author | string | No | Author name |
| keywords | string | No | Search keywords |
| limit | int | No | Max results (default: 10) |

**Request Body (POST):**
```json
{
  "title": "Wings of Fire",
  "author": "Tui T. Sutherland",
  "limit": 5
}
```

**Response:**
```json
{
  "query": "Wings of Fire Tui T. Sutherland",
  "total_results": 3,
  "results": [
    {
      "title": "Wings of Fire",
      "author": "Tui T. Sutherland",
      "isbn": "9780545125764",
      "source": "open_library",
      "url": "https://openlibrary.org...",
      "cover_url": "https://...",
      "availability": "available",
      "confidence": 0.95
    }
  ]
}
```

---

### Get Book Details

**GET** `/books/{isbn}`

Get detailed information about a specific book.

**Response:**
```json
{
  "isbn": "9780545125764",
  "title": "Wings of Fire",
  "author": "Tui T. Sutherland",
  "source": "open_library",
  "url": "https://openlibrary.org/works/OL...",
  "cover_url": "https://...",
  "pages": 480,
  "language": "en",
  "available": true
}
```

---

## PDF Generation Endpoints

### Generate PDF Excerpt

**POST** `/pdf/generate`

Generate a 2-page PDF excerpt from a book.

**Request Body:**
```json
{
  "session_id": "abc12345",
  "title": "Wings of Fire"
}
```

**Response:**
```json
{
  "session_id": "abc12345",
  "book_title": "Wings of Fire",
  "query": "I want to read Wings...",
  "pdf_size_bytes": 15432,
  "download_url": "/api/v1/pdf/download/abc12345",
  "status": "generated"
}
```

---

### Check PDF Status

**GET** `/pdf/status/{job_id}`

Check the status of a PDF generation job.

**Response:**
```json
{
  "job_id": "abc12345",
  "status": "completed",
  "progress": 100
}
```

---

### Download PDF

**GET** `/pdf/download/{job_id}`

Download the generated PDF file.

**Response:** PDF file content (binary)

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Provide at least one search term (title, author, or keywords)"
}
```

### 404 Not Found
```json
{
  "detail": "Session not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Model loading error: Model file not found"
}
```

---

## Rate Limiting

- **Limit:** 100 requests per minute per session
- **Headers:**
  ```
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1721486400
  ```

---

## Authentication (Optional)

Future versions will support API key authentication:

**Header:**
```
X-API-Key: your_api_key_here
```

---

## Examples

### Complete Voice Query Flow

```bash
# 1. Start recording
curl -X POST http://localhost:8000/api/v1/voice/record \
  -H "Content-Type: application/json" \
  -d '{"max_duration": 60}'

# Response: {"session_id": "abc123", ...}

# 2. Stop recording and transcribe
curl -X POST http://localhost:8000/api/v1/voice/stop/abc123 \
  -H "Content-Type: application/json" \
  -d '{"continue_search": true}'

# Response: {"transcript": "I want to read...", ...}

# 3. Search for the book
curl http://localhost:8000/api/v1/books/search \
  -H "Content-Type: application/json" \
  -d '{"title": "Wings of Fire"}'

# Response: {"results": [...]}

# 4. Generate PDF
curl -X POST http://localhost:8000/api/v1/pdf/generate \
  -H "Content-Type: application/json" \
  -d '{"session_id": "abc123", "title": "Wings of Fire"}'

# Response: {"download_url": "...", ...}
```

---

## API Versioning

The API uses URL path versioning:

- `/api/v1/voice/record` - Current version
- Future: `/api/v2/voice/record`

Breaking changes will increment the major version number.

---

**Last Updated:** 2026-07-20  
**API Version:** 1.0.0  
**Status:** Stable
