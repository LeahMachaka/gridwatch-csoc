// dashboard/static/js/dashboard.js — clock, score bars, Chart.js

document.addEventListener("DOMContentLoaded", function () {
  feather.replace();

  updateClock();
  setInterval(updateClock, 1000);

  colourScoreBars();

  initCharts();
});

function updateClock() {
  var clockElement = document.getElementById("live-clock");
  if (!clockElement) return;

  var now = new Date();
  var hours = String(now.getUTCHours()).padStart(2, "0");
  var minutes = String(now.getUTCMinutes()).padStart(2, "0");
  var seconds = String(now.getUTCSeconds()).padStart(2, "0");

  clockElement.textContent = hours + ":" + minutes + ":" + seconds + " UTC";
}

function colourScoreBars() {
  var bars = document.querySelectorAll(".score-bar-fill");

  bars.forEach(function (bar) {
    var widthString = bar.style.width;
    var score = parseInt(widthString, 10);

    if (score >= 80) {
      bar.classList.add("score-crit");
    } else if (score >= 60) {
      bar.classList.add("score-high");
    } else if (score >= 40) {
      bar.classList.add("score-medium");
    } else {
      bar.classList.add("score-low");
    }
  });
}

function initCharts() {
  if (typeof Chart === "undefined") return;

  var elZ = document.getElementById("gw-data-zones");
  var elS = document.getElementById("gw-data-severity");
  if (!elZ || !elS) return;

  var zones = JSON.parse(elZ.textContent);
  var severity = JSON.parse(elS.textContent);

  Chart.defaults.color = "#a3a3a3";
  Chart.defaults.borderColor = "rgba(255,255,255,0.06)";
  Chart.defaults.font.family = "'Inter', system-ui, sans-serif";

  var ctxDonut = document.getElementById("chart-severity");
  if (ctxDonut && severity.labels && severity.labels.length) {
    new Chart(ctxDonut, {
      type: "doughnut",
      data: {
        labels: severity.labels,
        datasets: [
          {
            data: severity.values,
            backgroundColor: severity.colors && severity.colors.length ? severity.colors : ["#ef4444", "#f97316", "#eab308", "#22c55e"],
            borderWidth: 0,
            hoverOffset: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "62%",
        plugins: {
          legend: {
            position: "right",
            labels: { boxWidth: 10, padding: 12, font: { size: 11 } },
          },
        },
      },
    });
  }

  var ctxBar = document.getElementById("chart-zones");
  if (ctxBar && zones.labels && zones.labels.length) {
    new Chart(ctxBar, {
      type: "bar",
      data: {
        labels: zones.labels,
        datasets: [
          {
            label: "Devices",
            data: zones.values,
            backgroundColor: "#14b8a6",
            borderRadius: 4,
            borderSkipped: false,
          },
        ],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            beginAtZero: true,
            grid: { color: "rgba(255,255,255,0.06)" },
            ticks: { font: { size: 11 } },
          },
          y: {
            grid: { display: false },
            ticks: { font: { size: 11 } },
          },
        },
        plugins: {
          legend: { display: false },
        },
      },
    });
  }
}
