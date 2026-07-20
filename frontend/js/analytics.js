let timelineChart = null;
let distributionChart = null;

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function renderTimelineChart(timeline) {
  const ctx = document.getElementById("chart-timeline");
  const labels = timeline.map((t) => t.mes);
  const counts = timeline.map((t) => t.cantidad);

  if (timelineChart) timelineChart.destroy();
  timelineChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Reseñas por mes",
        data: counts,
        borderColor: cssVar("--series-blue"),
        backgroundColor: cssVar("--series-blue") + "26",
        borderWidth: 2,
        pointRadius: 3,
        fill: true,
        tension: 0.25,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: cssVar("--gridline") }, ticks: { color: cssVar("--text-muted") } },
        y: { beginAtZero: true, grid: { color: cssVar("--gridline") }, ticks: { color: cssVar("--text-muted") } },
      },
    },
  });
}

function renderDistributionChart(distribucion) {
  const ctx = document.getElementById("chart-distribution");
  const orderedStars = [5, 4, 3, 2, 1];
  const byStars = Object.fromEntries(distribucion.map((d) => [d.estrellas, d.cantidad]));
  const counts = orderedStars.map((s) => byStars[s] || 0);

  if (distributionChart) distributionChart.destroy();
  distributionChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: orderedStars.map((s) => `${s} ★`),
      datasets: [{
        label: "Reseñas",
        data: counts,
        backgroundColor: cssVar("--series-blue"),
        borderRadius: 4,
        maxBarThickness: 46,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: cssVar("--text-muted") } },
        y: { beginAtZero: true, grid: { color: cssVar("--gridline") }, ticks: { color: cssVar("--text-muted") } },
      },
    },
  });
}

function renderKeywords(keywords) {
  const container = document.getElementById("keywords-list");
  container.innerHTML = keywords
    .map((k) => `<span class="keyword-chip"><b>${k.palabra}</b> · ${k.frecuencia}</span>`)
    .join("");
}
