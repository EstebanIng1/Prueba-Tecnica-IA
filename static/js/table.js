// table.js — Filtros, búsqueda y ordenamiento

document.addEventListener("DOMContentLoaded", function () {
  const tableBody    = document.getElementById('tableBody');
  const searchInput  = document.getElementById('searchInput');
  const catFilter    = document.getElementById('categoryFilter');
  const ratingFilter = document.getElementById('ratingFilter');
  const countLabel   = document.getElementById('countLabel');

  if (!tableBody) { console.error("No se encontró tableBody"); return; }

  const allRows = Array.from(tableBody.querySelectorAll('tr'));
  console.log("Filas encontradas:", allRows.length);

  // Poblar dropdown de categorías dinámicamente
  const cats = [...new Set(allRows.map(r => r.dataset.category))].filter(c => c && c !== 'undefined' && c !== 'N/A');
  console.log("Categorías:", cats);

  cats.forEach(c => {
    const opt = document.createElement('option');
    opt.value = c;
    opt.textContent = c.split('/').pop().charAt(0).toUpperCase() + c.split('/').pop().slice(1);
    catFilter.appendChild(opt);
  });

  // Si no hay categorías múltiples, ocultar el filtro
  if (cats.length <= 1) {
    catFilter.style.display = 'none';
  }

  let sortCol = null;
  let sortAsc = true;

  function applyFilters() {
    const search = searchInput.value.toLowerCase().trim();
    const cat    = catFilter.value;
    const rating = ratingFilter.value ? parseInt(ratingFilter.value) : 0;
    let visible  = 0;

    allRows.forEach(row => {
      const rowName   = (row.dataset.name   || '').toLowerCase();
      const rowCat    = (row.dataset.category || '');
      const rowRating = parseInt(row.dataset.rating) || 0;

      // Get text from first cell as fallback for search
      const cellText = (row.cells[0] ? row.cells[0].textContent : '').toLowerCase();

      const matchSearch = !search || rowName.includes(search) || cellText.includes(search);
      const matchCat    = !cat    || rowCat === cat;
      const matchRating = !rating || rowRating >= rating;

      const show = matchSearch && matchCat && matchRating;
      row.style.display = show ? '' : 'none';
      if (show) visible++;
    });

    countLabel.textContent = visible + ' de ' + allRows.length + ' productos';
  }

  function sortTable(col) {
    sortAsc = sortCol === col ? !sortAsc : true;
    sortCol = col;

    document.querySelectorAll('thead th.sortable').forEach(th => {
      th.classList.remove('sorted-asc', 'sorted-desc');
      if (th.dataset.col === col) th.classList.add(sortAsc ? 'sorted-asc' : 'sorted-desc');
    });

    const sorted = [...allRows].sort((a, b) => {
      let va, vb;
      if (col === 'price') {
        va = parseFloat(a.dataset.price) || 0;
        vb = parseFloat(b.dataset.price) || 0;
      } else if (col === 'rating') {
        va = parseInt(a.dataset.rating) || 0;
        vb = parseInt(b.dataset.rating) || 0;
      } else if (col === 'name') {
        va = (a.cells[0] ? a.cells[0].textContent : '').toLowerCase();
        vb = (b.cells[0] ? b.cells[0].textContent : '').toLowerCase();
      } else {
        va = (a.dataset[col] || '').toLowerCase();
        vb = (b.dataset[col] || '').toLowerCase();
      }
      return va < vb ? (sortAsc ? -1 : 1) : va > vb ? (sortAsc ? 1 : -1) : 0;
    });

    sorted.forEach(row => tableBody.appendChild(row));
  }

  // Event listeners
  searchInput.addEventListener('input', applyFilters);
  catFilter.addEventListener('change', applyFilters);
  ratingFilter.addEventListener('change', applyFilters);

  document.querySelectorAll('thead th.sortable').forEach(th =>
    th.addEventListener('click', () => sortTable(th.dataset.col))
  );

  // Inicializar
  applyFilters();
  console.log("table.js inicializado OK");
});