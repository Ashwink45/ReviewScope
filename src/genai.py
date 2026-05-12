from huggingface_hub import InferenceClient
import json
from dotenv import load_dotenv
import os


# --------------------------------------------------
# Hugging Face Client
# --------------------------------------------------

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    api_key=HF_TOKEN
)


# --------------------------------------------------
# Generate AI Insight
# --------------------------------------------------

def generate_ai_insight(reviews):

    # ----------------------------------------------
    # Extract NEGATIVE reviews only
    # ----------------------------------------------

    negative_reviews = []

    for r in reviews:

        if r.get("model_sentiment") == "NEGATIVE":

            text = r.get("review")

            if text and len(text.split()) > 5:

                negative_reviews.append(text)

    # ----------------------------------------------
    # No negative reviews
    # ----------------------------------------------

    if not negative_reviews:

        print("No negative reviews to process.")

        return {
            "summary": "No major negative trends detected.",
            "top_issue": "None",
            "severity": "Low",
            "issue_keywords": []
        }

    # ----------------------------------------------
    # Take representative samples
    # ----------------------------------------------

    sample_reviews = negative_reviews[:5]

    combined_reviews = "\n".join(sample_reviews)

    # ----------------------------------------------
    # Prompt Engineering
    # ----------------------------------------------

    prompt = f"""
You are an AI product analyst.

Analyze the following negative Play Store reviews
and identify recurring user frustrations,
technical failures, and product instability issues.

Return your response ONLY in valid JSON format.

Required JSON structure:

{{
    "summary": "Detailed professional insight summary explaining the major user complaints and recurring problems.",

    "top_issue": "Most critical recurring issue detected",

    "severity": "Low/Moderate/High",

    "issue_keywords": [
        "keyword1",
        "keyword2",
        "keyword3"
    ]
}}

Guidelines:
- Keep the summary professional and concise.
- Focus on recurring patterns across reviews.
- issue_keywords should contain short issue tags only.
- Do not include explanations outside JSON.

Reviews:
{combined_reviews}
"""

    # ----------------------------------------------
    # PRINT INPUT PROMPT
    # ----------------------------------------------

    print("\n" + "=" * 50)
    print("🚀 SENDING INPUT TO GENAI")
    print("=" * 50)

    print(prompt)

    print("=" * 50 + "\n")

    # ----------------------------------------------
    # Generate Summary
    # ----------------------------------------------

    try:

        result = client.chat_completion(

            model="Qwen/Qwen2.5-7B-Instruct",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            max_tokens=400
        )

        # ------------------------------------------
        # PRINT RAW OUTPUT
        # ------------------------------------------

        print("\n" + "=" * 50)
        print("✅ RAW GENAI OUTPUT")
        print("=" * 50)

        print(result)

        print("=" * 50 + "\n")

        # ------------------------------------------
        # Extract AI content only
        # ------------------------------------------

        ai_text = result.choices[0].message.content

        # ------------------------------------------
        # Clean markdown formatting
        # ------------------------------------------

        ai_text = ai_text.replace("```json", "")
        ai_text = ai_text.replace("```", "")
        ai_text = ai_text.strip()

        # ------------------------------------------
        # PRINT CLEAN JSON TEXT
        # ------------------------------------------

        print("\n" + "=" * 50)
        print("🧠 CLEAN AI JSON")
        print("=" * 50)

        print(ai_text)

        print("=" * 50 + "\n")

        # ------------------------------------------
        # Parse JSON safely
        # ------------------------------------------

        try:

            ai_data = json.loads(ai_text)

        except Exception as parse_error:

            print("JSON PARSE ERROR:", parse_error)

            ai_data = {
                "summary": "AI parsing failed.",
                "top_issue": "Unknown",
                "severity": "Unknown",
                "issue_keywords": []
            }

        # ------------------------------------------
        # PRINT FINAL PARSED OUTPUT
        # ------------------------------------------

        print("\n" + "=" * 50)
        print("✅ FINAL PARSED AI DATA")
        print("=" * 50)

        print(ai_data)

        print("=" * 50 + "\n")

        return ai_data

    # ----------------------------------------------
    # Exception Handling
    # ----------------------------------------------

    except Exception as e:

        print("GENAI ERROR:", e)

        return {
            "summary": "Unable to generate AI insight.",
            "top_issue": "Unknown",
            "severity": "Unknown",
            "issue_keywords": []
        }


# --------------------------------------------------
# TEST RUNNER
# --------------------------------------------------

if __name__ == "__main__":

    dummy_reviews = [

        {
            "model_sentiment": "NEGATIVE",
            "review":
            "It keeps crashing on my TV after 10 minutes."
        },

        {
            "model_sentiment": "NEGATIVE",
            "review":
            "Instagram logged me out of all devices."
        },

        {
            "model_sentiment": "NEGATIVE",
            "review":
            "Notifications are delayed and reels freeze."
        },

        {
            "model_sentiment": "POSITIVE",
            "review":
            "The app works perfectly fine for me."
        }
    ]

    print("🚀 Starting GenAI test...\n")

    result = generate_ai_insight(dummy_reviews)

    print("\nFINAL RETURNED DATA:")
    print(result)