let chart4 = null;

function updateChart4(summary) {
  const canvas = document.getElementById("Chart4");

  if (!canvas) {
    console.error("Canvas not found");
    return;
  }

  const ctx = canvas.getContext("2d");

  if (chart4) chart4.destroy();

  chart4 = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Positive", "Negative"],
      datasets: [{
        label: "Reviews",
        data: [
          summary?.positive || 0,
          summary?.negative || 0
        ],
        backgroundColor: ["#22c55e", "#ef4444"]
      }]
    }
  });
}

let versionChart = null;

function updateVersionChart(stats) {
  const canvas = document.getElementById("VersionChart");

  if (!canvas) {
    console.error("VersionChart canvas not found");
    return;
  }

  const ctx = canvas.getContext("2d");

  // destroy old chart if exists
  if (versionChart) versionChart.destroy();

  versionChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: stats.labels,
      datasets: [
        {
          label: "Positive",
          data: stats.positiveData,
          backgroundColor: "#22c55e",
          stack: "reviews"
        },
        {
          label: "Negative",
          data: stats.negativeData,
          backgroundColor: "#ef4444",
          stack: "reviews"
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          display: true
        },
        tooltip: {
          mode: "index",
          intersect: false
        }
      },
      scales: {
        x: {
          stacked: true,
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        },
        y: {
          stacked: true,
          beginAtZero: true
        }
      }
    }
  });
}

let hourlySpikeChart = null;

function updateHourlySpikeChart(stats) {

  const canvas = document.getElementById("HourlySpikeChart");

  if (!canvas) {
    console.error("HourlySpikeChart canvas not found");
    return;
  }

  const ctx = canvas.getContext("2d");

  // destroy old chart before creating new one
  if (hourlySpikeChart) {
    hourlySpikeChart.destroy();
  }

  hourlySpikeChart = new Chart(ctx, {

    type: "line",

    data: {
      labels: stats.labels,

      datasets: [
        {
          label: "Negative Reviews",

          data: stats.data,

          borderColor: "#ef4444",
          backgroundColor: "rgba(239, 68, 68, 0.2)",

          fill: true,

          tension: 0.4,

          pointRadius: 4,
          pointHoverRadius: 6,

          borderWidth: 3
        }
      ]
    },

    options: {

      responsive: true,

      plugins: {

        legend: {
          display: true
        },

        tooltip: {
          mode: "index",
          intersect: false
        }
      },

      scales: {

        x: {
          title: {
            display: true,
            text: "Hour of Day"
          },

          ticks: {
            callback: function(value) {
              return value + ":00";
            }
          }
        },

        y: {
          beginAtZero: true,

          title: {
            display: true,
            text: "Negative Review Count"
          }
        }
      }
    }
  });
}
let scatterChart = null;

function updateScatterChart(dataPoints, mode) {

  const canvas = document.getElementById("Chart1");

  if (!canvas) {
    console.error("Chart1 canvas not found");
    return;
  }

  const ctx = canvas.getContext("2d");

  // destroy old chart
  if (scatterChart) {
    scatterChart.destroy();
  }

  scatterChart = new Chart(ctx, {

    type: "scatter",

    data: {

      datasets: [
        {
          label:
            mode === "NEGATIVE"
              ? "Negative Reviews"
              : "Positive Reviews",

          data: dataPoints,

          backgroundColor:
            mode === "NEGATIVE"
              ? "#ef4444"
              : "#22c55e",

          borderColor:
            mode === "NEGATIVE"
              ? "#dc2626"
              : "#16a34a",

          pointRadius: 6,
          pointHoverRadius: 9
        }
      ]
    },

    options: {

      responsive: true,
      maintainAspectRatio: false,

      plugins: {

        legend: {
          display: true
        },

        tooltip: {

          callbacks: {

            label: function(context) {

              const point = context.raw;

              return (point.review || "").substring(0, 900);
              
            }
          }
        }
      },

      scales: {

        x: {

          title: {
            display: true,
            text: "Review Index"
          }
        },

        y: {

          beginAtZero: true,

          title: {
            display: true,
            text: "Word Count"
          }
        }
      }
    }
  });
}