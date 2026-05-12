# AI Review Intelligence Dashboard

An AI-powered dashboard that analyzes live Google Play Store reviews using sentiment analysis and LLM-based issue summarization.

## Features

- Live Play Store review scraping
- Sentiment analysis using DistilBERT
- AI-generated issue summaries using Qwen 2.5
- Interactive analytics dashboard
- FastAPI backend
- Docker deployment support

## Technologies Used

- Python
- FastAPI
- Hugging Face Transformers
- DistilBERT
- Qwen 2.5
- Google Play Scraper
- HTML/CSS/JavaScript
- Bootstrap
- Chart.js
- Docker

## Run Locally

```bash
uvicorn src.main:app --host 0.0.0.0 --port 7860