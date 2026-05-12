import polars as pl

df = pl.read_parquet("data/gold/reviews_with_sentiment.parquet")

# 1. Sentiment distribution
sentiment_dist = df.group_by("model_sentiment").count()

# 2. Rating vs model sentiment mismatch
df = df.with_columns([
    (pl.col("sentiment_category").str.to_uppercase() != pl.col("model_sentiment")).alias("mismatch")
])

mismatch_stats = df.group_by("mismatch").count()

# 3. Avg rating by sentiment
avg_rating = df.group_by("model_sentiment").agg(
    pl.col("rating").mean()
)

# 4. Reviews by day
reviews_by_day = df.group_by("day_of_week").count()

print(sentiment_dist)
print(mismatch_stats)
print(avg_rating)
print(reviews_by_day)