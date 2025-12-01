const BASE = 'http://localhost:8000';

// Variables globales para edición
let editingInsumoId = null;
let editingEmpleadoId = null;

// Fetch helper
async function apiRequest(method, endpoint, data = null) {
  const url = `${BASE}${endpoint}`;
  const options = {
    method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (data) options.body = JSON.stringify(data);

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Error ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// Cargar todos los datos
async function loadData() {
  try {
    const [insumos, empleados, entregas] = await Promise.all([
      apiRequest('GET', '/inventario/insumos'),
      apiRequest('GET', '/rrhh/empleados'),
      apiRequest('GET', '/distribucion/entregas')
    ]);

    // Calcular métricas
    const valorInsumos = insumos.reduce((sum, i) => sum + (i.stock?.actual || 0), 0);
    const empleadosActivos = empleados.filter(e => e.estado === 'activo').length;
    const entregasHoy = entregas.length; // Simplificado, sin fecha
    const alertasStock = insumos.filter(i => {
      const actual = i.stock?.actual || 0;
      return actual <= 0 || actual <= (i.stock?.min || 0);
    }).length;

    // Actualizar métricas
    document.getElementById('valor-insumos').textContent = valorInsumos;
    document.getElementById('empleados-activos').textContent = empleadosActivos;
    document.getElementById('entregas-hoy').textContent = entregasHoy;
    document.getElementById('alertas-stock').textContent = alertasStock;

    // Renderizar tablas
    renderInsumos(insumos);
    renderEmpleados(empleados);
    renderEntregas(entregas, empleados, insumos);

  } catch (error) {
    console.error('Error loading data:', error);
  }
}

// Renderizar insumos
function renderInsumos(insumos) {
  const tbody = document.getElementById('insumos-tbody');
  tbody.innerHTML = '';

  insumos.forEach(insumo => {
    const stockActual = insumo.stock?.actual || 0;
    const stockMin = insumo.stock?.min || 0;
    const stockMax = insumo.stock?.max || 0;
    let estado, rowClass;
    if (stockActual <= 0) {
      estado = 'Sin Stock';
      rowClass = 'no-stock-row';
    } else if (stockActual <= stockMin) {
      estado = 'Crítico';
      rowClass = 'critical-row';
    } else if (stockActual <= stockMax) {
      estado = 'OK';
      rowClass = 'ok-row';
    } else {
      estado = 'Exceso';
      rowClass = 'excess-row';
    }

    const row = document.createElement('tr');
    row.className = rowClass;
    row.innerHTML = `
      <td>${insumo.nombre}</td>
      <td>${insumo.categoria}</td>
      <td>${stockActual}</td>
      <td>${stockMin}</td>
      <td>${insumo.stock?.max || 0}</td>
      <td>${estado}</td>
      <td>
        <button class="action-btn edit-btn" data-id="${insumo.id}">✏️</button>
        <button class="action-btn update-stock-btn" data-id="${insumo.id}">📦</button>
        <button class="action-btn delete-btn" data-id="${insumo.id}">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });

  // Event listeners
  tbody.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => editInsumo(e.target.dataset.id));
  });
  tbody.querySelectorAll('.update-stock-btn').forEach(btn => {
    btn.addEventListener('click', (e) => updateStock(e.target.dataset.id));
  });
  tbody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => deleteInsumo(e.target.dataset.id));
  });
}

// Renderizar empleados
function renderEmpleados(empleados) {
  const tbody = document.getElementById('empleados-tbody');
  tbody.innerHTML = '';

  empleados.forEach(empleado => {
    const rowClass = empleado.estado === 'activo' ? 'active-row' : 'inactive-row';
    const toggleIcon = empleado.estado === 'activo' ? '🔴' : '⚫'; // on/off

    const row = document.createElement('tr');
    row.className = rowClass;
    row.innerHTML = `
      <td>${empleado.cedula}</td>
      <td>${empleado.estado}</td>
      <td>${empleado.nombre_completo}</td>
      <td>${empleado.cargo}</td>
      <td>${empleado.departamento}</td>
      <td>${empleado.email}</td>
      <td>${empleado.telefono}</td>
      <td>
        <button class="action-btn edit-btn" data-id="${empleado.id}">✏️</button>
        <button class="action-btn toggle-status-btn" data-id="${empleado.id}">${toggleIcon}</button>
        <button class="action-btn delete-btn" data-id="${empleado.id}">🗑️</button>
      </td>
    `;
    tbody.appendChild(row);
  });

  // Event listeners
  tbody.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => editEmpleado(e.target.dataset.id));
  });
  tbody.querySelectorAll('.toggle-status-btn').forEach(btn => {
    btn.addEventListener('click', (e) => toggleEmpleadoStatus(e.target.dataset.id));
  });
  tbody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => deleteEmpleado(e.target.dataset.id));
  });
}

// Renderizar entregas
function renderEntregas(entregas, empleados, insumos) {
  const tbody = document.getElementById('entregas-tbody');
  tbody.innerHTML = '';

  const empleadoMap = empleados.reduce((map, e) => { map[e.id] = e.nombre_completo; return map; }, {});
  const insumoMap = insumos.reduce((map, i) => { map[i.id] = i.nombre; return map; }, {});

  entregas.forEach(entrega => {
    const empleadoNombre = empleadoMap[entrega.empleado_id] || 'Desconocido';
    const insumoNombre = insumoMap[entrega.insumo_id] || 'Desconocido';

    let actions = `
      <button class="action-btn delete-btn" data-id="${entrega.id}">🗑️</button>
    `;
    if (entrega.estado === 'PENDIENTE') {
      actions = `<button class="action-btn confirm-btn" data-id="${entrega.id}">✅</button>` + actions;
    }

    const rowClass = entrega.estado === 'PENDIENTE' ? 'pending-row' : entrega.estado === 'CONFIRMADA' ? 'confirmed-row' : '';

    const row = document.createElement('tr');
    row.className = rowClass;
    row.innerHTML = `
      <td>${empleadoNombre}</td>
      <td>${insumoNombre}</td>
      <td>${entrega.cantidad}</td>
      <td>${entrega.estado}</td>
      <td>${actions}</td>
    `;
    tbody.appendChild(row);
  });

  // Event listeners
  tbody.querySelectorAll('.confirm-btn').forEach(btn => {
    btn.addEventListener('click', (e) => confirmEntrega(e.target.dataset.id));
  });
  tbody.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', (e) => deleteEntrega(e.target.dataset.id));
  });
}

// Funciones CRUD Insumos
function openInsumoModal() {
  editingInsumoId = null;
  document.getElementById('insumo-modal-title').textContent = 'Nuevo Insumo';
  document.getElementById('insumo-form').reset();
  document.getElementById('insumo-modal').style.display = 'block';
}

async function editInsumo(id) {
  try {
    const insumo = await apiRequest('GET', `/inventario/insumos/${id}`);
    editingInsumoId = id;
    document.getElementById('insumo-modal-title').textContent = 'Editar Insumo';
    document.getElementById('insumo-nombre').value = insumo.nombre;
    document.getElementById('insumo-categoria').value = insumo.categoria;
    document.getElementById('insumo-stock-actual').value = insumo.stock.actual;
    document.getElementById('insumo-stock-min').value = insumo.stock.min;
    document.getElementById('insumo-stock-max').value = insumo.stock.max;
    document.getElementById('insumo-modal').style.display = 'block';
  } catch (error) {
    console.error('Error loading insumo:', error);
  }
}

async function updateStock(id) {
  const newStock = prompt('Ingrese nueva cantidad de stock actual:');
  if (newStock !== null && !isNaN(newStock)) {
    try {
      const insumo = await apiRequest('GET', `/inventario/insumos/${id}`);
      const data = {
        nombre: insumo.nombre,
        categoria: insumo.categoria,
        stock_actual: parseInt(newStock),
        stock_min: insumo.stock.min,
        stock_max: insumo.stock.max
      };
      await apiRequest('PUT', `/inventario/insumos/${id}`, data);
      loadData();
    } catch (error) {
      console.error('Error updating stock:', error);
    }
  }
}

async function deleteInsumo(id) {
  if (confirm('¿Eliminar insumo?')) {
    try {
      await apiRequest('DELETE', `/inventario/insumos/${id}`);
      loadData();
    } catch (error) {
      console.error('Error deleting insumo:', error);
    }
  }
}

document.getElementById('insumo-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    nombre: document.getElementById('insumo-nombre').value,
    categoria: document.getElementById('insumo-categoria').value,
    stock_actual: parseInt(document.getElementById('insumo-stock-actual').value),
    stock_min: parseInt(document.getElementById('insumo-stock-min').value),
    stock_max: parseInt(document.getElementById('insumo-stock-max').value)
  };

  try {
    if (editingInsumoId) {
      await apiRequest('PUT', `/inventario/insumos/${editingInsumoId}`, data);
    } else {
      await apiRequest('POST', '/inventario/insumos', data);
    }
    document.getElementById('insumo-modal').style.display = 'none';
    loadData();
  } catch (error) {
    console.error('Error saving insumo:', error);
  }
});

// Funciones CRUD Empleados
function openEmpleadoModal() {
  editingEmpleadoId = null;
  document.getElementById('empleado-modal-title').textContent = 'Nuevo Empleado';
  document.getElementById('empleado-form').reset();
  document.getElementById('empleado-modal').style.display = 'block';
}

async function editEmpleado(id) {
  try {
    const empleado = await apiRequest('GET', `/rrhh/empleados/${id}`);
    editingEmpleadoId = id;
    document.getElementById('empleado-modal-title').textContent = 'Editar Empleado';
    document.getElementById('empleado-cedula').value = empleado.cedula;
    document.getElementById('empleado-estado').value = empleado.estado;
    document.getElementById('empleado-nombre').value = empleado.nombre_completo;
    document.getElementById('empleado-cargo').value = empleado.cargo;
    document.getElementById('empleado-departamento').value = empleado.departamento;
    document.getElementById('empleado-email').value = empleado.email;
    document.getElementById('empleado-telefono').value = empleado.telefono;
    document.getElementById('empleado-modal').style.display = 'block';
  } catch (error) {
    console.error('Error loading empleado:', error);
  }
}

async function toggleEmpleadoStatus(id) {
  try {
    const empleado = await apiRequest('GET', `/rrhh/empleados/${id}`);
    const newStatus = empleado.estado === 'activo' ? 'inactivo' : 'activo';
    const data = {
      cedula: empleado.cedula,
      estado: newStatus,
      nombre_completo: empleado.nombre_completo,
      cargo: empleado.cargo,
      departamento: empleado.departamento,
      email: empleado.email,
      telefono: empleado.telefono
    };
    await apiRequest('PUT', `/rrhh/empleados/${id}`, data);
    loadData();
  } catch (error) {
    console.error('Error toggling status:', error);
  }
}

async function deleteEmpleado(id) {
  if (confirm('¿Eliminar empleado?')) {
    try {
      await apiRequest('DELETE', `/rrhh/empleados/${id}`);
      loadData();
    } catch (error) {
      console.error('Error deleting empleado:', error);
    }
  }
}

document.getElementById('empleado-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    cedula: document.getElementById('empleado-cedula').value,
    estado: document.getElementById('empleado-estado').value,
    nombre_completo: document.getElementById('empleado-nombre').value,
    cargo: document.getElementById('empleado-cargo').value,
    departamento: document.getElementById('empleado-departamento').value,
    email: document.getElementById('empleado-email').value,
    telefono: document.getElementById('empleado-telefono').value
  };

  try {
    if (editingEmpleadoId) {
      await apiRequest('PUT', `/rrhh/empleados/${editingEmpleadoId}`, data);
    } else {
      await apiRequest('POST', '/rrhh/empleados', data);
    }
    document.getElementById('empleado-modal').style.display = 'none';
    loadData();
  } catch (error) {
    console.error('Error saving empleado:', error);
  }
});

// Funciones CRUD Entregas
async function openEntregaModal() {
  try {
    const [empleados, insumos] = await Promise.all([
      apiRequest('GET', '/rrhh/empleados'),
      apiRequest('GET', '/inventario/insumos')
    ]);

    const empleadoSelect = document.getElementById('entrega-empleado');
    empleadoSelect.innerHTML = '<option value="">Seleccionar Empleado</option>';
    empleados.forEach(e => {
      empleadoSelect.innerHTML += `<option value="${e.id}">${e.nombre_completo}</option>`;
    });

    const insumoSelect = document.getElementById('entrega-insumo');
    insumoSelect.innerHTML = '<option value="">Seleccionar Insumo</option>';
    insumos.forEach(i => {
      insumoSelect.innerHTML += `<option value="${i.id}">${i.nombre}</option>`;
    });

    document.getElementById('entrega-modal').style.display = 'block';
  } catch (error) {
    console.error('Error loading options:', error);
  }
}

async function confirmEntrega(id) {
  try {
    const entrega = await apiRequest('GET', `/distribucion/entregas/${id}`);
    const insumo = await apiRequest('GET', `/inventario/insumos/${entrega.insumo_id}`);
    if (insumo.stock.actual < entrega.cantidad) {
      alert('Stock insuficiente para confirmar la entrega.');
      return;
    }
    await apiRequest('POST', `/distribucion/entregas/${id}/confirmar`);
    // Actualizar stock automáticamente
    const newStock = insumo.stock.actual - entrega.cantidad;
    const data = {
      nombre: insumo.nombre,
      categoria: insumo.categoria,
      stock_actual: newStock,
      stock_min: insumo.stock.min,
      stock_max: insumo.stock.max
    };
    await apiRequest('PUT', `/inventario/insumos/${entrega.insumo_id}`, data);
    loadData();
  } catch (error) {
    console.error('Error confirming entrega:', error);
  }
}

async function deleteEntrega(id) {
  if (confirm('¿Eliminar entrega?')) {
    try {
      await apiRequest('DELETE', `/distribucion/entregas/${id}`);
      loadData();
    } catch (error) {
      console.error('Error deleting entrega:', error);
    }
  }
}

document.getElementById('entrega-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = {
    empleado_id: document.getElementById('entrega-empleado').value,
    insumo_id: document.getElementById('entrega-insumo').value,
    cantidad: parseInt(document.getElementById('entrega-cantidad').value)
  };

  try {
    await apiRequest('POST', '/distribucion/entregas', data);
    document.getElementById('entrega-modal').style.display = 'none';
    loadData();
  } catch (error) {
    console.error('Error creating entrega:', error);
  }
});

// Event listeners iniciales
document.addEventListener('DOMContentLoaded', () => {
  loadData();

  // Botones nuevos
  document.getElementById('nuevo-insumo-btn').addEventListener('click', openInsumoModal);
  document.getElementById('nuevo-empleado-btn').addEventListener('click', openEmpleadoModal);
  document.getElementById('nueva-entrega-btn').addEventListener('click', openEntregaModal);

  // Cerrar modales
  document.querySelectorAll('.modal-close').forEach(close => {
    close.addEventListener('click', () => {
      document.querySelectorAll('.modal').forEach(modal => modal.style.display = 'none');
    });
  });

  window.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
      e.target.style.display = 'none';
    }
  });
});