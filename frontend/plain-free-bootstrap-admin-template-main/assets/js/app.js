let fakeProgress = 0;

let progressInterval;

function startLoaderAnimation() {

  fakeProgress = 0;

  clearInterval(progressInterval);

  const loader =
    document.getElementById("topLoader");

  const progressBar =
    document.getElementById("topProgressBar");

  const loadingStatus =
    document.getElementById("loadingStatus");

  loader.style.display = "block";

  loadingStatus.style.display = "block";

  progressBar.style.width = "0%";

  // FAST INITIAL BURST

  setTimeout(() => {

    fakeProgress = 18;

    progressBar.style.width =
      `${fakeProgress}%`;

  }, 100);

  // SLOW NATURAL MOVEMENT

  progressInterval = setInterval(() => {

    if (fakeProgress < 75) {

      fakeProgress +=
        Math.random() * 4;

      progressBar.style.width =
        `${fakeProgress}%`;
    }

  }, 400);
}

function finishLoaderAnimation() {

  const loader =
    document.getElementById("topLoader");

  const progressBar =
    document.getElementById("topProgressBar");

  const loadingStatus =
    document.getElementById("loadingStatus");

  clearInterval(progressInterval);

  // FINISH TO 100%
  progressBar.style.width = "100%";

  setTimeout(() => {

    loader.style.opacity = "0";

    loadingStatus.style.opacity = "0";

    setTimeout(() => {

      loader.style.display = "none";

      loadingStatus.style.display = "none";

      loader.style.opacity = "1";

      loadingStatus.style.opacity = "1";

      progressBar.style.width = "0%";

    }, 300);

  }, 350);
}

async function analyzeApp(event) {
  event.preventDefault();

  // -------------------------------
  // START LOADER
  // -------------------------------

  startLoaderAnimation();

  let appName = document.getElementById("appInput").value.trim();

  if (!appName) {
    alert("Enter app name");
    return;
  }

  document.getElementById("appNameDisplay").innerText = appName.toUpperCase();



  try {
    const res = await fetch("/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ app_id: appName })
    });

    const data = await res.json();
  
    console.log(data);
    console.log("AI INSIGHTS:", data.ai_insights);

    // ----------------------------------
    // AI INSIGHTS
    // ----------------------------------

    const ai =
      data.ai_insights || {};


    // ----------------------------------
    // SUMMARY
    // ----------------------------------

    const aiSummary =
      document.getElementById("aiSummary");

    if (aiSummary) {
      aiSummary.innerText =
        ai.summary || "No AI summary available";
    }


    // ----------------------------------
    // RISK LEVEL
    // ----------------------------------

    const riskLevel =
      document.getElementById("riskLevel");

    if (riskLevel) {
      riskLevel.innerText =
        ai.severity || "Unknown";
    }


    // ----------------------------------
    // TOP ISSUE
    // ----------------------------------

    const criticalIssue =
      document.getElementById("criticalIssue");

    if (criticalIssue) {
      criticalIssue.innerText =
        ai.top_issue || "No issues detected";
    }


    // ----------------------------------
    // ISSUE TAGS
    // ----------------------------------

    const tagsContainer =
      document.getElementById("issueTags");

    if (tagsContainer) {

      tagsContainer.innerHTML = "";

      (ai.issue_keywords || []).forEach(tag => {

        tagsContainer.innerHTML += `

      <span
        class="
          badge
          bg-primary
        "
      >
        ${tag}
      </span>

    `;

      });
    }

    // 🔥 handle backend error
    if (data.error) {
      alert(data.error);
      return;
    }

    const summary = data.summary;

    const mapping = {
      positiveReviews: "positive",
      negativeReviews: "negative",
      totalReviews: "total_reviews"
    };

    for (let id in mapping) {
      const el = document.getElementById(id);
      if (el) {
        el.innerText = summary[mapping[id]];
      }
    }

    const mismatch =
      summary.total_reviews -
      (summary.positive + summary.negative);

    document.getElementById("mismatchReviews").innerText = mismatch;

    // charts
    updateChart4(summary);
    //version chart
    const versionStats = processVersionData(data.data);
    updateVersionChart(versionStats);

    //HOURLY ANOMALY CHART
    const hourlyStats = processHourlyNegativeData(data.data);
    updateHourlySpikeChart(hourlyStats);

    // SCATTERPLOT
    window.allReviews = data.data;

    const scatterMode =
      document.getElementById("scatterMode").value;

    const scatterData =
      processScatterData(data.data, scatterMode);

    updateScatterChart(scatterData, scatterMode);

    finishLoaderAnimation();

  } catch (err) {
    finishLoaderAnimation();
    console.error("Error:", err);
  }
}

function processVersionData(reviews) {
  const versionMap = {};

  reviews.forEach(r => {
    const version = r.version || "Unknown";

    if (!versionMap[version]) {
      versionMap[version] = { positive: 0, negative: 0 };
    }

    if (r.model_sentiment === "POSITIVE") {
      versionMap[version].positive++;
    } else {
      versionMap[version].negative++;
    }
  });

  // Convert to arrays
  let labels = Object.keys(versionMap);

  // 🔥 OPTIONAL: sort versions (simple string sort for now)
  labels.sort();

  // 🔥 OPTIONAL: limit to last 6 versions (clean UI)
  labels = labels.slice(-6);

  const positiveData = labels.map(v => versionMap[v].positive);
  const negativeData = labels.map(v => versionMap[v].negative);

  return { labels, positiveData, negativeData };
}

function processHourlyNegativeData(reviews) {

  // create 24-hour buckets
  const hourlyCounts = new Array(24).fill(0);

  reviews.forEach(r => {

    // only count NEGATIVE reviews
    if (r.model_sentiment === "NEGATIVE") {

      const hour = r.hour;

      if (hour >= 0 && hour <= 23) {
        hourlyCounts[hour]++;
      }
    }
  });

  return {
    labels: Array.from({ length: 24 }, (_, i) => i),
    data: hourlyCounts
  };
}

function processScatterData(reviews, mode = "NEGATIVE") {

  const filtered = reviews.filter(r =>
    r.model_sentiment === mode
  );

  return filtered.map((r, index) => ({
    x: index + 1,

    y: r.word_count,

    review: r.review,

    rating: r.rating,

    date: r.date
  }));
}

document.addEventListener("DOMContentLoaded", () => {

  const dropdown =
    document.getElementById("scatterMode");

  if (!dropdown) return;

  dropdown.addEventListener("change", () => {

    if (!window.allReviews) return;

    const mode = dropdown.value;

    const scatterData =
      processScatterData(window.allReviews, mode);

    updateScatterChart(scatterData, mode);
  });
});