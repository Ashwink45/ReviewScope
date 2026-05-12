from src.scraper import fetch_reviews
from src.process import process_reviews
from src.sentiment import add_sentiment
from src.genai import generate_ai_insight

def run_pipeline(app_id: str):

    # -----------------------------
    # Step 1: Scrape
    # -----------------------------
    raw = fetch_reviews(app_id)

    if not raw:
        return {
            "error": "Invalid app ID or no reviews found"
        }

    # -----------------------------
    # Step 2: Process
    # -----------------------------
    df = process_reviews(raw)

    # -----------------------------
    # Step 3: Sentiment
    # -----------------------------
    df = add_sentiment(df)

    # -----------------------------
    # Step 4: GenAI Insight
    # -----------------------------

    ai_summary = generate_ai_insight(
        df.to_dicts()
        )   
    # -----------------------------
    # Step 4: Summary
    # -----------------------------
    positive = df.filter(df["model_sentiment"] == "POSITIVE").height
    negative = df.filter(df["model_sentiment"] == "NEGATIVE").height

    # -----------------------------
    # Final Output
    # -----------------------------
    return {
        "app_id": app_id,
        "summary": {
            "total_reviews": df.height,
            "positive": positive,
            "negative": negative
        },
        "ai_insights": ai_summary,
        "data": df.to_dicts()
    }