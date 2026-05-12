from transformers import pipeline
import polars as pl

# -----------------------------
# Load model ONCE (global)
# -----------------------------
model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# -----------------------------
# Function
# -----------------------------
def add_sentiment(df: pl.DataFrame):

    reviews = df["clean_review"].to_list()

    # Run inference
    results = model(reviews, batch_size=16)

    # Extract outputs
    labels = [r["label"] for r in results]
    scores = [r["score"] for r in results]

    # Safety check
    if len(labels) != len(df):
        raise ValueError("Mismatch in prediction length")

    # Add columns
    df = df.with_columns([
        pl.Series("model_sentiment", labels),
        pl.Series("model_score", scores)
    ])

    return df