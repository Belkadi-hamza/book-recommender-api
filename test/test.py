import requests
import json

# URL of your API
url = "http://127.0.0.1:8000/api/v1/recommendations"

# Example request payload
payload = {
    "domain": "computer science",
    "modules": ["machine learning", "python", "data mining"],
    "limit": 5
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise exception for HTTP errors

    data = response.json()

    if data.get("status") == "success":
        print(f"✅ {data['count']} recommendations received:\n")
        print("=" * 80)
        for rec in data["recommendations"]:
            print(f"\n📚 Rank {rec['rank']}:")
            print(f"   Title: {rec['title']}")
            print(f"   Price: ${rec['price']}" if rec['price'] else "   Price: N/A")
            print(f"   Review Score: {rec['review_score']}" if rec['review_score'] else "   Review Score: N/A")
            print(f"   Review Summary: {rec['review_summary']}" if rec['review_summary'] else "   Review Summary: N/A")
            print(f"   Similarity Score: {rec['score']}")
            print("-" * 80)
    else:
        print("❌ API returned an error:", data)

except requests.exceptions.RequestException as e:
    print("❌ Request failed:", e)
