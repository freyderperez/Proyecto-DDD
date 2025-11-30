let editingEmpleadoId = null;

document.addEventListener('DOMContentLoaded', loadEmpleados);

document.getElementById('empleadoForm').addEventListener('submit', handleFormSubmit);

async function loadEmpleados() {
  try {
    console.log('Cargando empleados...');
    const empleados = await apiRequest('GET', '/rrhh/empleados');
    console.log('Empleados cargados:', empleados);
    displayEmpleados(empleados);
  } catch (error) {
    console.error('Error loading empleados:', error);
  }
}

function displayEmpleados(empleados) {
  const tbody = document.getElementById('empleadosBody');
  tbody.innerHTML = '';

  empleados.forEach(empleado => {
    const row = document.createElement('tr');

    row.innerHTML = `
      <td>${empleado.id}</td>
      <td>${empleado.cedula}</td>
      <td>${empleado.estado}</td>
      <td>${empleado.nombre_completo}</td>
      <td>${empleado.cargo}</td>
      <td>${empleado.departamento}</td>
      <td>${empleado.email}</td>
      <td>${empleado.telefono}</td>
      <td>
        <button class="btn btn-secondary" onclick="editEmpleado('${empleado.id}')">Editar</button>
        <button class="btn btn-danger" onclick="deleteEmpleado('${empleado.id}')">Eliminar</button>
      </td>
    `;

    tbody.appendChild(row);
  });
}

function openCreateModal() {
  editingEmpleadoId = null;
  document.getElementById('modalTitle').textContent = 'Crear Empleado';
  document.getElementById('empleadoForm').reset();
  document.getElementById('empleadoModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('empleadoModal').style.display = 'none';
  editingEmpleadoId = null;
}

async function editEmpleado(id) {
  try {
    const empleado = await apiRequest('GET', `/rrhh/empleados/${id}`);
    editingEmpleadoId = id;
    document.getElementById('modalTitle').textContent = 'Editar Empleado';
    document.getElementById('cedula').value = empleado.cedula;
    document.getElementById('estado').value = empleado.estado;
    document.getElementById('nombre_completo').value = empleado.nombre_completo;
    document.getElementById('cargo').value = empleado.cargo;
    document.getElementById('departamento').value = empleado.departamento;
    document.getElementById('email').value = empleado.email;
    document.getElementById('telefono').value = empleado.telefono;
    document.getElementById('empleadoModal').style.display = 'block';
  } catch (error) {
    console.error('Error loading empleado for edit:', error);
  }
}

async function handleFormSubmit(event) {
  event.preventDefault();

  const formData = {
    cedula: document.getElementById('cedula').value,
    estado: document.getElementById('estado').value,
    nombre_completo: document.getElementById('nombre_completo').value,
    cargo: document.getElementById('cargo').value,
    departamento: document.getElementById('departamento').value,
    email: document.getElementById('email').value,
    telefono: document.getElementById('telefono').value,
  };

  try {
    if (editingEmpleadoId) {
      await apiRequest('PUT', `/rrhh/empleados/${editingEmpleadoId}`, formData);
      showToast('Empleado actualizado exitosamente', 'success');
    } else {
      await apiRequest('POST', '/rrhh/empleados', formData);
      showToast('Empleado creado exitosamente', 'success');
    }
    closeModal();
    loadEmpleados();
  } catch (error) {
    console.error('Error saving empleado:', error);
    // Error ya mostrado por apiRequest
  }
}

async function deleteEmpleado(id) {
  if (confirm('¿Estás seguro de que quieres eliminar este empleado?')) {
    try {
      await apiRequest('DELETE', `/rrhh/empleados/${id}`);
      showToast('Empleado eliminado exitosamente', 'success');
      loadEmpleados();
    } catch (error) {
      console.error('Error deleting empleado:', error);
      // Error ya mostrado por apiRequest
    }
  }
}