from google_play_scraper import reviews, Sort
from langdetect import detect
from google_play_scraper import search


def get_app_id(app_id: str):

    print("SEARCHING FOR:", app_id)

    if "." in app_id:
        return app_id

    try:

        results = search(
            app_id,
            lang="en",
            country="us",
            n_hits=5
        )

        print("SEARCH RESULTS:", results)

        if not results:
            return None

        # 🔥 find FIRST VALID appId
        for app in results:

            if app.get("appId"):

                return app["appId"]

        return None

    except Exception as e:

        print("SEARCH ERROR:", e)

        return None

def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False


def fetch_reviews(app_id: str, count: int = 100):

    print("INPUT:", app_id)

    # Resolve package ID
    real_app_id = get_app_id(app_id)

    print("REAL APP ID:", real_app_id)

    if not real_app_id:
        print("FAILED TO RESOLVE APP ID")
        return []

    try:

        result, _ = reviews(
            real_app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=count
        )

        print("RAW REVIEWS:", len(result))

    except Exception as e:

        print("SCRAPER ERROR:", e)

        return []

    cleaned = []

    for r in result:

        text = r["content"]

        if text:

            cleaned.append({
                "review": text,
                "rating": r["score"],
                "date": str(r["at"]),
                "version": r.get("appVersion")
            })

    print("CLEANED REVIEWS:", len(cleaned))

    return cleaned