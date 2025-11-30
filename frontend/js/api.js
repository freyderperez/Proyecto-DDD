// Función central para hacer peticiones al API Gateway
async function apiRequest(method, endpoint, data = null) {
  // En Docker, usar el nombre del servicio; localmente localhost
  const baseURL = window.location.hostname === 'localhost' ? 'http://localhost:8000' : 'http://ms-gateway:8000';
  const url = `${baseURL}${endpoint}`;

  const options = {
    method: method.toUpperCase(),
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (data && (method.toUpperCase() === 'POST' || method.toUpperCase() === 'PUT')) {
    options.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error ${response.status}: ${errorText || response.statusText}`);
    }

    // Para DELETE, no hay body
    if (method.toUpperCase() === 'DELETE') {
      return { success: true };
    }

    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    } else {
      return await response.text();
    }
  } catch (error) {
    console.error('API Request Error:', error);
    showToast(`Error: ${error.message}`, 'error');
    throw error;
  }
}

// Función para mostrar toasts
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;

  const container = document.getElementById('toast-container');
  if (container) {
    container.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 3000);
  } else {
    alert(message); // Fallback
  }
}