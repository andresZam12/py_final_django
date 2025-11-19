// JavaScript para gráficas y funcionalidades interactivas
// Control de Proyectos y Tareas

// Función para inicializar gráficas con Chart.js
function initCharts() {
    console.log('Inicializando gráficas...');
}

// Función para confirmar eliminación
function confirmarEliminacion(mensaje) {
    return confirm(mensaje || '¿Estás seguro de realizar esta acción?');
}

// Auto-cerrar alertas después de 5 segundos
document.addEventListener('DOMContentLoaded', function() {
    // Auto-cerrar alertas
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Tooltip de Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Inicializar gráficas si existen
    initCharts();
});

// Función para actualizar progreso dinámicamente (AJAX)
function actualizarProgreso(proyectoId) {
    fetch(`/api/proyectos/${proyectoId}/estadisticas/`)
        .then(response => response.json())
        .then(data => {
            console.log('Progreso actualizado:', data);
            // Aquí puedes actualizar el DOM con los datos
        })
        .catch(error => console.error('Error:', error));
}

// Validación de formularios personalizada
function validarFormulario(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return false;
    }
    
    return true;
}

// Función para búsqueda en tiempo real (opcional)
function busquedaEnTiempoReal(inputId, listaId) {
    const input = document.getElementById(inputId);
    const lista = document.getElementById(listaId);
    
    if (!input || !lista) return;
    
    input.addEventListener('keyup', function() {
        const filtro = this.value.toLowerCase();
        const items = lista.getElementsByTagName('li');
        
        Array.from(items).forEach(item => {
            const texto = item.textContent || item.innerText;
            if (texto.toLowerCase().indexOf(filtro) > -1) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Función para copiar al portapapeles
function copiarAlPortapapeles(texto) {
    navigator.clipboard.writeText(texto).then(() => {
        alert('Copiado al portapapeles');
    }).catch(err => {
        console.error('Error al copiar:', err);
    });
}

// Exportar funciones para uso global
window.confirmarEliminacion = confirmarEliminacion;
window.actualizarProgreso = actualizarProgreso;
window.validarFormulario = validarFormulario;
window.busquedaEnTiempoReal = busquedaEnTiempoReal;
window.copiarAlPortapapeles = copiarAlPortapapeles;
