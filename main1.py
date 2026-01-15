from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import pickle
import requests
import io

# -----------------------------
# Configuration
# -----------------------------
MODEL_URL = "https://drive.google.com/uc?export=download&id=1jR5h4E5CZfZWpGCwNqdq-i_19M62L75c"  # Direct download link

# -----------------------------
# FastAPI instance
# -----------------------------
app = FastAPI(
    title="Book Recommendation API",
    description="Professional API for recommending books using TF-IDF & cosine similarity.",
    version="1.0.0",
    docs_url="/",       # Swagger UI at root
    redoc_url="/redoc"  # ReDoc at /redoc
)

# Enable CORS (optional, needed if frontend calls API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"]
)

# -----------------------------
# Load model from Google Drive
# -----------------------------
def load_model_from_drive(url: str):
    print("Downloading model from Google Drive...")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download model. Status code: {response.status_code}")
    # Load the pickle from bytes
    return pickle.load(io.BytesIO(response.content))

tfidf, tfidf_matrix_books, df_books_meta = load_model_from_drive(MODEL_URL)
print("Model loaded successfully.")

# -----------------------------
# Pydantic schemas
# -----------------------------
class RecommendationRequest(BaseModel):
    domain: str = Field(..., json_schema_extra={"example": "computer science"})
    modules: List[str] = Field(..., json_schema_extra={"example": ["machine learning", "python", "data mining"]})
    limit: int = Field(..., gt=0, le=20, json_schema_extra={"example": 5})

class Recommendation(BaseModel):
    rank: int
    title: str
    price: Optional[float] = None
    review_score: Optional[float] = None
    review_summary: Optional[str] = None
    score: float

class RecommendationResponse(BaseModel):
    status: str
    count: int
    recommendations: List[Recommendation]

# -----------------------------
# Recommendation endpoint
# -----------------------------
@app.post("/api/v1/recommendations", response_model=RecommendationResponse,
          summary="Get book recommendations",
          description="Returns a ranked list of recommended books based on domain and studied modules.")
def recommend_books(payload: RecommendationRequest):

    if not payload.modules:
        raise HTTPException(status_code=400, detail="Modules list cannot be empty.")

    # Create user text
    user_text = " ".join([payload.domain] + payload.modules)

    # Vectorize
    user_vector = tfidf.transform([user_text])

    # Cosine similarity
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix_books).flatten()

    # Top-N
    top_indices = similarity_scores.argsort()[-payload.limit:][::-1]

    # Build response with book details
    recommendations = []
    for i, idx in enumerate(top_indices):
        book = df_books_meta.iloc[idx]
        recommendations.append(
            Recommendation(
                rank=i + 1,
                title=str(book.get("book_title", "N/A")),
                price=float(book["book_price"]) if pd.notna(book.get("book_price")) else None,
                review_score=float(book["review_score"]) if pd.notna(book.get("review_score")) else None,
                review_summary=str(book.get("review_summary", "")) if pd.notna(book.get("review_summary")) else None,
                score=round(float(similarity_scores[idx]), 4)
            )
        )

    return RecommendationResponse(
        status="success",
        count=len(recommendations),
        recommendations=recommendations
    )

# -----------------------------
# Optional root redirect to Swagger
# -----------------------------
@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/")
