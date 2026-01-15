from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# -----------------------------
# FastAPI instance
# -----------------------------
app = FastAPI(
    title="Book Recommendation API",
    description="Professional API for recommending books using TF-IDF & cosine similarity.",
    version="1.0.0",
    docs_url="/",       # Swagger at root
    redoc_url="/redoc"  # Optional ReDoc
)

# -----------------------------
# Load the model
# -----------------------------
with open("recommender_model.pkl", "rb") as f:
    tfidf, tfidf_matrix_books, df_books_meta = pickle.load(f)

# -----------------------------
# Pydantic schemas
# -----------------------------
class RecommendationRequest(BaseModel):
    domain: str = Field(..., json_schema_extra={"example": "computer science"})
    modules: List[str] = Field(..., json_schema_extra={"example": ["machine learning", "python", "data mining"]})
    limit: int = Field(..., gt=0, le=20, json_schema_extra={"example": 5})

class Recommendation(BaseModel):
    rank: int
    book_id: str
    score: float

class RecommendationResponse(BaseModel):
    status: str
    count: int
    recommendations: List[Recommendation]

# -----------------------------
# Helper for error response
# -----------------------------
def error_response(message: str, status_code: int = 400):
    return {"status": "error", "message": message}, status_code

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

    # Build response
    recommendations = [
        Recommendation(
            rank=i + 1,
            book_id=str(df_books_meta.iloc[idx]["book_id"]),
            score=round(float(similarity_scores[idx]), 4)
        )
        for i, idx in enumerate(top_indices)
    ]

    return RecommendationResponse(
        status="success",
        count=len(recommendations),
        recommendations=recommendations
    )
