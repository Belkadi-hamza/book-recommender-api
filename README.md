# Book Recommendation API

A professional FastAPI-based REST API for recommending books using TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity algorithms.

## Overview

This API provides intelligent book recommendations based on a user's domain of interest and studied modules. It uses machine learning techniques to find the most relevant books by analyzing text similarity between user preferences and book metadata.

## Features

- **FastAPI Framework**: Modern, fast, and auto-documented REST API
- **TF-IDF Algorithm**: Advanced text vectorization for content analysis
- **Cosine Similarity**: Mathematical approach to find relevant books
- **Input Validation**: Robust request validation using Pydantic
- **Interactive Documentation**: Built-in Swagger UI and ReDoc
- **Ranking System**: Returns top-N recommendations with similarity scores
- **Cloud-based Model**: Model loaded from Google Drive for easy deployment
- **Rich Book Details**: Returns title, price, reviews, and similarity scores

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/Belkadi-hamza/book-recommender-api.git
cd book-recommender-api
```

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
```

3. **Activate the virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Prerequisites

The trained model file `recommender_model.pkl` is automatically downloaded from Google Drive when the API starts. The model contains:
- TF-IDF vectorizer
- TF-IDF matrix for books
- Books metadata DataFrame

## Running the API

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc
- **API Endpoint**: http://localhost:8000/api/v1/recommendations

### Production Deployment

For production, run without the `--reload` flag:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Usage

### Endpoint

**POST** `/api/v1/recommendations`

### Request Body

```json
{
  "domain": "computer science",
  "modules": ["machine learning", "python", "data mining"],
  "limit": 5
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `domain` | string | Yes | The main domain of interest |
| `modules` | array[string] | Yes | List of studied modules/topics (cannot be empty) |
| `limit` | integer | Yes | Number of recommendations to return (1-20) |

### Response

```json
{
  "status": "success",
  "count": 5,
  "recommendations": [
    {
      "rank": 1,
      "title": "Machine Learning with Python",
      "price": 49.99,
      "review_score": 4.5,
      "review_summary": "Excellent book for beginners",
      "score": 0.8542
    },
    {
      "rank": 2,
      "title": "Data Mining Techniques",
      "price": 39.99,
      "review_score": 4.2,
      "review_summary": "Comprehensive guide to data mining",
      "score": 0.7821
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Request status ("success" or "error") |
| `count` | integer | Number of recommendations returned |
| `recommendations` | array | List of recommended books |
| `rank` | integer | Ranking position (1 = best match) |
| `title` | string | Book title |
| `price` | float/null | Book price (null if not available) |
| `review_score` | float/null | Average review score (null if not available) |
| `review_summary` | string/null | Review summary text (null if not available) |
| `score` | float | Similarity score (0.0 - 1.0, higher is better) |

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/v1/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "domain": "computer science",
    "modules": ["machine learning", "python", "data mining"],
    "limit": 5
  }'
```

### Using Python

```python
import requests

url = "http://localhost:8000/api/v1/recommendations"
payload = {
    "domain": "computer science",
    "modules": ["machine learning", "python", "data mining"],
    "limit": 5
}

response = requests.post(url, json=payload)
data = response.json()

if data["status"] == "success":
    for book in data["recommendations"]:
        print(f"{book['rank']}. {book['title']} - Score: {book['score']}")
```

### Using JavaScript

```javascript
fetch('http://localhost:8000/api/v1/recommendations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    domain: 'computer science',
    modules: ['machine learning', 'python', 'data mining'],
    limit: 5
  })
})
.then(response => response.json())
.then(data => {
  data.recommendations.forEach(book => {
    console.log(`${book.rank}. ${book.title} - $${book.price}`);
  });
});
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid input (e.g., empty modules list, invalid limit)
- **422 Unprocessable Entity**: Validation error (e.g., incorrect data types)
- **500 Internal Server Error**: Server-side errors

Example error response:
```json
{
  "detail": "Modules list cannot be empty."
}
```

## Project Structure

```
book-recommender-api/
├── main.py                    # Main FastAPI application
├── requirements.txt           # Python dependencies
├── vercel.json               # Vercel deployment configuration
├── README.md                 # Project documentation
├── .gitignore               # Git ignore file
├── test/
│   └── test.py              # API test script
└── __pycache__/             # Python cache files
```

## Technology Stack

- **FastAPI**: Modern web framework for building APIs
- **Pydantic**: Data validation and settings management
- **scikit-learn**: Machine learning library (TF-IDF, cosine similarity)
- **pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Uvicorn**: ASGI server for running the application
- **Google Drive**: Cloud storage for ML model

## Algorithm Details

1. **Model Loading**: ML model is downloaded from Google Drive on startup
2. **Text Combination**: User's domain and modules are combined into a single text
3. **TF-IDF Vectorization**: Text is converted into numerical vectors
4. **Cosine Similarity**: Similarity scores are calculated between user vector and all book vectors
5. **Ranking**: Books are ranked by similarity score in descending order
6. **Top-N Selection**: The top N books (based on limit) are returned with full details

## Deployment

### Vercel

The API is configured for deployment on Vercel:

1. Push your code to GitHub
2. Import the repository in Vercel dashboard
3. Configure:
   - **Install Command**: `pip install -r requirements.txt`
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
4. Deploy

The model will be automatically downloaded from Google Drive on the first request.

### Alternative Platforms

This API can also be deployed on:
- **Railway** (https://railway.app)
- **Render** (https://render.com)
- **Fly.io** (https://fly.io)
- **Heroku**
- **AWS Lambda** with API Gateway

## Testing

Run the test script to verify the API is working:

```bash
python test/test.py
```

## Development

To modify or extend the API:

1. Edit [main.py](main.py) for API logic changes
2. Update models/schemas in the Pydantic classes
3. Test changes using the interactive docs at http://localhost:8000/
4. Run with `--reload` flag for auto-reloading during development

## License

This project is part of an academic exercise for "Méthode Agile" course.

## Contributing

This is an academic project. For suggestions or improvements, please contact the project maintainer.

## Support

For issues or questions, please refer to the interactive API documentation at http://localhost:8000/ when the server is running.

## Author

**Belkadi Hamza**
- GitHub: [@Belkadi-hamza](https://github.com/Belkadi-hamza)
