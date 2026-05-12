import polars as pl
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def process_reviews(data):
    # data = list of dicts from scraper

    df = pl.DataFrame(data)

    # -----------------------------
    # TEXT CLEANING
    # -----------------------------
    df = df.with_columns([
        pl.col("review").map_elements(clean_text).alias("clean_review")
    ])

    # -----------------------------
    # REVIEW LENGTH
    # -----------------------------
    df = df.with_columns([
        pl.col("clean_review").str.len_chars().alias("char_count"),
        pl.col("clean_review").str.split(" ").list.len().alias("word_count")
    ])

    # -----------------------------
    # SENTIMENT CATEGORY (from rating)
    # -----------------------------
    df = df.with_columns([
        pl.when(pl.col("rating") <= 2).then(pl.lit("Negative"))
        .when(pl.col("rating") == 3).then(pl.lit("Neutral"))
        .otherwise(pl.lit("Positive"))
        .alias("sentiment_category")
    ])

    # -----------------------------
    # TIME FEATURES
    # -----------------------------
    df = df.with_columns([
        pl.col("date").str.strptime(pl.Datetime, strict=False).alias("parsed_date")
    ])

    df = df.with_columns([
        pl.col("parsed_date").dt.hour().alias("hour"),
        pl.col("parsed_date").dt.weekday().alias("day_of_week")
    ])

    # -----------------------------
    # VERSION FLAG
    # -----------------------------
    df = df.with_columns([
        pl.col("version").is_null().alias("is_version_missing")
    ])

    return df