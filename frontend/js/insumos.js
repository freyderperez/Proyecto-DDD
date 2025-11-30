let editingInsumoId = null;

document.addEventListener('DOMContentLoaded', loadInsumos);

document.getElementById('insumoForm').addEventListener('submit', handleFormSubmit);

async function loadInsumos() {
  try {
    console.log('Cargando insumos...');
    const insumos = await apiRequest('GET', '/inventario/insumos');
    console.log('Insumos cargados:', insumos);
    displayInsumos(insumos);
  } catch (error) {
    console.error('Error loading insumos:', error);
  }
}

function displayInsumos(insumos) {
  const tbody = document.getElementById('insumosBody');
  tbody.innerHTML = '';

  insumos.forEach(insumo => {
    const rowClass = getStockClass(insumo.stock);
    const row = document.createElement('tr');
    row.className = rowClass;

    row.innerHTML = `
      <td>${insumo.id}</td>
      <td>${insumo.nombre}</td>
      <td>${insumo.categoria}</td>
      <td>${insumo.stock.actual}</td>
      <td>${insumo.stock.min}</td>
      <td>${insumo.stock.max}</td>
      <td>
        <button class="btn btn-secondary" onclick="editInsumo('${insumo.id}')">Editar</button>
        <button class="btn btn-danger" onclick="deleteInsumo('${insumo.id}')">Eliminar</button>
      </td>
    `;

    tbody.appendChild(row);
  });
}

function getStockClass(stock) {
  if (stock.actual < stock.min) return 'stock-low';
  if (stock.actual === stock.min) return 'stock-warning';
  return '';
}

function openCreateModal() {
  editingInsumoId = null;
  document.getElementById('modalTitle').textContent = 'Crear Insumo';
  document.getElementById('insumoForm').reset();
  document.getElementById('insumoModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('insumoModal').style.display = 'none';
  editingInsumoId = null;
}

async function editInsumo(id) {
  try {
    const insumo = await apiRequest('GET', `/inventario/insumos/${id}`);
    editingInsumoId = id;
    document.getElementById('modalTitle').textContent = 'Editar Insumo';
    document.getElementById('nombre').value = insumo.nombre;
    document.getElementById('categoria').value = insumo.categoria;
    document.getElementById('stock_actual').value = insumo.stock.actual;
    document.getElementById('stock_min').value = insumo.stock.min;
    document.getElementById('stock_max').value = insumo.stock.max;
    document.getElementById('insumoModal').style.display = 'block';
  } catch (error) {
    console.error('Error loading insumo for edit:', error);
  }
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const formData = {
    nombre: document.getElementById('nombre').value,
    categoria: document.getElementById('categoria').value,
    stock_actual: parseInt(document.getElementById('stock_actual').value),
    stock_min: parseInt(document.getElementById('stock_min').value),
    stock_max: parseInt(document.getElementById('stock_max').value),
  };

  try {
    if (editingInsumoId) {
      await apiRequest('PUT', `/inventario/insumos/${editingInsumoId}`, formData);
      showToast('Insumo actualizado exitosamente', 'success');
    } else {
      await apiRequest('POST', '/inventario/insumos', formData);
      showToast('Insumo creado exitosamente', 'success');
    }
    closeModal();
    loadInsumos();
  } catch (error) {
    console.error('Error saving insumo:', error);
    // Error ya mostrado por apiRequest
  }
}

async function deleteInsumo(id) {
  if (confirm('¿Estás seguro de que quieres eliminar este insumo?')) {
    try {
      await apiRequest('DELETE', `/inventario/insumos/${id}`);
      showToast('Insumo eliminado exitosamente', 'success');
      loadInsumos();
    } catch (error) {
      console.error('Error deleting insumo:', error);
      // Error ya mostrado por apiRequest
    }
  }
}