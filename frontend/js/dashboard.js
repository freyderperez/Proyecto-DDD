// dashboard.js
const BASE = (window.__API_BASE__ || 'http://localhost:8000');

async function fetchJSON(url, options = {}) {
  const res = await fetch(url, {...options, headers: {'Content-Type':'application/json'}})
  if(!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

function fmtNum(n){
  if(n===null || n===undefined) return '—';
  return new Intl.NumberFormat('es-CO').format(Number(n));
}

function sanitizeName(name){
  return (name||'').toString().trim();
}

/**
 * Determina el estado de stock:
 * critical: actual < min
 * warning: actual == min
 * ok: actual > min
 */
function stockStatus(actual, min){
  if(actual == null || min == null) return 'ok';
  const a = Number(actual), m = Number(min);
  if(a < m) return 'critical';
  if(a === m) return 'warning';
  return 'ok';
}

async function loadInsumos() {
  const tbody = document.getElementById('insumosTbody');
  tbody.innerHTML = '';
  try {
    const data = await fetchJSON(`${BASE}/inventario/insumos`);
    // cards: compute metrics
    const totalInsumos = data.length;
    const alerts = data.filter(i => stockStatus(i.stock?.actual, i.stock?.min) === 'critical').length;
    const valorInsumos = data.reduce((acc, i) => acc + (Number(i.stock?.actual || 0)), 0); // ejemplo simple

    document.getElementById('card-valor-insumos').textContent = fmtNum(valorInsumos);
    document.getElementById('card-alertas').textContent = alerts;

    // load empleados
    try {
      const empleados = await fetchJSON(`${BASE}/rrhh/empleados`);
      const activos = empleados.filter(e => e.estado === 'Activo').length;
      document.getElementById('card-empleados').textContent = activos;
    } catch (err) {
      console.error('Error cargando empleados', err);
      document.getElementById('card-empleados').textContent = '—';
    }

    // load entregas (total, ya que no hay fecha)
    try {
      const entregas = await fetchJSON(`${BASE}/distribucion/entregas`);
      document.getElementById('card-entregas').textContent = entregas.length;
    } catch (err) {
      console.error('Error cargando entregas', err);
      document.getElementById('card-entregas').textContent = '—';
    }

    // populate table rows
    data.forEach(insumo => {
      const tr = document.createElement('tr');

      const nombre = insumo.nombre || '—';
      const categoria = insumo.categoria || '—';
      const stockActual = insumo.stock?.actual ?? null;
      const stockMin = insumo.stock?.min ?? null;
      const stockMax = insumo.stock?.max ?? null;

      tr.innerHTML = `
        <td>${nombre}</td>
        <td>${categoria}</td>
        <td>${fmtNum(stockActual)}</td>
        <td>${fmtNum(stockMin)}</td>
        <td>${fmtNum(stockMax)}</td>
        <td>${renderStockBadge(stockStatus(stockActual, stockMin))}</td>
        <td>
          <button class="action-btn edit" data-id="${insumo.id}" title="Editar">✎</button>
          <button class="action-btn delete" data-id="${insumo.id}" title="Eliminar">🗑</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    // attach listeners for edit/delete
    tbody.querySelectorAll('.edit').forEach(b => b.addEventListener('click', onEdit));
    tbody.querySelectorAll('.delete').forEach(b => b.addEventListener('click', onDelete));

  } catch (err) {
    console.error('Error cargando insumos', err);
    alert('Error cargando insumos: ' + (err.message || err));
  }
}

function renderStockBadge(status){
  if(status === 'critical') return `<span class="badge critical">Crítico</span>`;
  if(status === 'warning') return `<span class="badge warning">En límite</span>`;
  return `<span class="badge ok">OK</span>`;
}

async function onEdit(e){
  const id = e.currentTarget.dataset.id;
  // abrir modal o navegar a página de edición
  alert('Editar: ' + id);
}

async function onDelete(e){
  const id = e.currentTarget.dataset.id;
  if(!confirm('Confirmar eliminación?')) return;
  try{
    const res = await fetch(`${BASE}/inventario/insumos/${id}`, { method: 'DELETE' });
    if(!res.ok) throw new Error('Error en eliminación');
    await loadInsumos();
    alert('Eliminado');
  }catch(err){
    console.error(err);
    alert('Error eliminando: ' + err.message);
  }
}

// events
document.getElementById('refreshBtn').addEventListener('click', loadInsumos);

// initial load
loadInsumos();