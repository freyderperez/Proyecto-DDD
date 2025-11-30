let insumos = [];
let empleados = [];

document.addEventListener('DOMContentLoaded', async () => {
  await loadInsumos();
  await loadEmpleados();
  loadEntregas();
});

document.getElementById('entregaForm').addEventListener('submit', handleFormSubmit);

async function loadInsumos() {
  try {
    insumos = await apiRequest('GET', '/inventario/insumos');
    populateInsumoSelect();
  } catch (error) {
    console.error('Error loading insumos:', error);
  }
}

async function loadEmpleados() {
  try {
    empleados = await apiRequest('GET', '/rrhh/empleados');
    populateEmpleadoSelect();
  } catch (error) {
    console.error('Error loading empleados:', error);
  }
}

async function loadEntregas() {
  try {
    console.log('Cargando entregas...');
    const entregas = await apiRequest('GET', '/distribucion/entregas');
    console.log('Entregas cargadas:', entregas);
    displayEntregas(entregas);
  } catch (error) {
    console.error('Error loading entregas:', error);
  }
}

function displayEntregas(entregas) {
  const tbody = document.getElementById('entregasBody');
  tbody.innerHTML = '';

  entregas.forEach(entrega => {
    const empleadoNombre = empleados.find(e => e.id === entrega.empleado_id)?.nombre_completo || entrega.empleado_id;
    const insumoNombre = insumos.find(i => i.id === entrega.insumo_id)?.nombre || entrega.insumo_id;

    const row = document.createElement('tr');

    row.innerHTML = `
      <td>${entrega.id}</td>
      <td>${empleadoNombre}</td>
      <td>${insumoNombre}</td>
      <td>${entrega.cantidad}</td>
      <td>${entrega.estado}</td>
      <td>
        <button class="btn btn-danger" onclick="deleteEntrega('${entrega.id}')">Eliminar</button>
      </td>
    `;

    tbody.appendChild(row);
  });
}

function populateEmpleadoSelect() {
  const select = document.getElementById('empleado_id');
  select.innerHTML = '<option value="">Seleccionar Empleado</option>';
  empleados.forEach(empleado => {
    const option = document.createElement('option');
    option.value = empleado.id;
    option.textContent = empleado.nombre_completo;
    select.appendChild(option);
  });
}

function populateInsumoSelect() {
  const select = document.getElementById('insumo_id');
  select.innerHTML = '<option value="">Seleccionar Insumo</option>';
  insumos.forEach(insumo => {
    const option = document.createElement('option');
    option.value = insumo.id;
    option.textContent = insumo.nombre;
    select.appendChild(option);
  });
}

function openCreateModal() {
  document.getElementById('entregaForm').reset();
  document.getElementById('entregaModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('entregaModal').style.display = 'none';
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const formData = {
    empleado_id: document.getElementById('empleado_id').value,
    insumo_id: document.getElementById('insumo_id').value,
    cantidad_entregada: parseInt(document.getElementById('cantidad').value),
  };

  try {
    await apiRequest('POST', '/distribucion/entregas', formData);
    showToast('Entrega creada exitosamente', 'success');
    closeModal();
    loadEntregas();
  } catch (error) {
    console.error('Error creating entrega:', error);
    // Error ya mostrado por apiRequest
  }
}

async function deleteEntrega(id) {
  if (confirm('¿Estás seguro de que quieres eliminar esta entrega?')) {
    try {
      await apiRequest('DELETE', `/distribucion/entregas/${id}`);
      showToast('Entrega eliminada exitosamente', 'success');
      loadEntregas();
    } catch (error) {
      console.error('Error deleting entrega:', error);
      // Error ya mostrado por apiRequest
    }
  }
}