// charts.js — Gráficas Chart.js
// Lee CHART_DATA del objeto global inyectado por dashboard.py

document.addEventListener("DOMContentLoaded", function () {
  const { names, prices, ratingDist } = window.CHART_DATA;

  const BDB_BLUE = '#003087';
  const BDB_RED  = '#CC0000';
  const BDB_GOLD = '#C8960C';
  const GRID     = 'rgba(0,0,0,0.06)';

  Chart.defaults.color = '#7a8aaa';
  Chart.defaults.font.family = "'DM Mono', monospace";

  const shortNames = names.map(n => n.length > 20 ? n.slice(0, 18) + '…' : n);

  // Barras — Precio por producto
  new Chart(document.getElementById('priceChart'), {
    type: 'bar',
    data: {
      labels: shortNames,
      datasets: [{
        label: 'Precio (USD)',
        data: prices,
        backgroundColor: prices.map(p => p === Math.max(...prices) ? BDB_GOLD : BDB_BLUE + 'cc'),
        borderColor: BDB_BLUE,
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { color: GRID }, ticks: { maxRotation: 45, font: { size: 9 } } },
        y: { grid: { color: GRID }, ticks: { callback: v => '$' + v } }
      }
    }
  });

  // Dona — Distribución de ratings
  new Chart(document.getElementById('ratingChart'), {
    type: 'doughnut',
    data: {
      labels: ['★ 1', '★★ 2', '★★★ 3', '★★★★ 4', '★★★★★ 5'],
      datasets: [{
        data: Object.values(ratingDist),
        backgroundColor: [BDB_RED + 'cc', BDB_GOLD + 'cc', '#5b8dd9cc', '#7a8aaacc', BDB_BLUE + 'cc'],
        borderColor: '#fff',
        borderWidth: 3,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: 'right', labels: { font: { size: 11 }, padding: 12 } }
      }
    }
  });
});