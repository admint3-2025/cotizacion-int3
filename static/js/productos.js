// Variables globales
let productos = [];
let categorias = [];
let modoEdicion = false;
let usuarioActual = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    verificarSesion();
});

// Verificar sesión
async function verificarSesion() {
    try {
        const response = await fetch('/api/session');
        const data = await response.json();
        
        if (!data.authenticated) {
            window.location.href = '/login';
            return;
        }
        
        usuarioActual = data.usuario;
        
        // Actualizar UI
        document.getElementById('nombreUsuario').textContent = usuarioActual.nombre_completo;
        
        // Mostrar botón de usuarios si es admin
        if (usuarioActual.rol === 'admin') {
            document.getElementById('btnUsuarios').style.display = 'inline-block';
        }
        
        // Cargar datos
        cargarCategorias();
        cargarProductos();
        
        // Event listeners
        document.getElementById('formProducto').addEventListener('submit', guardarProducto);
        
    } catch (error) {
        console.error('Error al verificar sesión:', error);
        window.location.href = '/login';
    }
}

// Cerrar sesión
async function cerrarSesion() {
    try {
        await fetch('/api/logout', {
            method: 'POST'
        });
        window.location.href = '/login';
    } catch (error) {
        console.error('Error al cerrar sesión:', error);
    }
}

// Cargar categorías
async function cargarCategorias() {
    try {
        const response = await fetch('/api/categorias');
        categorias = await response.json();
        
        // Actualizar select de filtro
        const selectFiltro = document.getElementById('filtroCategoria');
        selectFiltro.innerHTML = '<option value="">Todas</option>';
        categorias.forEach(cat => {
            selectFiltro.innerHTML += `<option value="${cat}">${cat}</option>`;
        });
        
        // Actualizar datalist del formulario
        const datalist = document.getElementById('categoriasList');
        datalist.innerHTML = '';
        categorias.forEach(cat => {
            datalist.innerHTML += `<option value="${cat}">`;
        });
        
    } catch (error) {
        console.error('Error al cargar categorías:', error);
    }
}

// Cargar lista de productos
async function cargarProductos() {
    try {
        const incluirInactivos = document.getElementById('mostrarInactivos').checked;
        const filtroTipo = document.getElementById('filtroTipo').value;
        const filtroCategoria = document.getElementById('filtroCategoria').value;
        
        const response = await fetch(`/api/productos?incluir_inactivos=${incluirInactivos}`);
        productos = await response.json();
        
        // Aplicar filtros
        let productosFiltrados = productos;
        
        if (filtroTipo) {
            productosFiltrados = productosFiltrados.filter(p => p.tipo === filtroTipo);
        }
        
        if (filtroCategoria) {
            productosFiltrados = productosFiltrados.filter(p => p.categoria === filtroCategoria);
        }
        
        const tbody = document.getElementById('tablaProductos');
        
        if (productosFiltrados.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8" class="empty-state">
                        <div>📦</div>
                        <p>No hay productos registrados</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = productosFiltrados.map(producto => `
            <tr data-codigo="${producto.codigo}" data-nombre="${producto.nombre.toLowerCase()}">
                <td><strong>${producto.codigo}</strong></td>
                <td>
                    <strong>${producto.nombre}</strong>
                    ${producto.descripcion ? `<br><small style="color: #666;">${producto.descripcion}</small>` : ''}
                </td>
                <td>
                    <span class="badge badge-${producto.tipo}">
                        ${producto.tipo === 'producto' ? '📦 Producto' : '⚙️ Servicio'}
                    </span>
                </td>
                <td>
                    ${producto.categoria ? `<span class="categoria-tag">${producto.categoria}</span>` : '-'}
                </td>
                <td><span class="precio">$${formatearPrecio(producto.precio)}</span></td>
                <td>${producto.unidad}</td>
                <td>
                    <span class="badge badge-${producto.activo ? 'activo' : 'inactivo'}">
                        ${producto.activo ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td>
                    <button class="btn-action btn-edit" onclick="editarProducto(${producto.id})">
                        Editar
                    </button>
                    <button class="btn-action btn-delete" onclick="eliminarProducto(${producto.id})">
                        Eliminar
                    </button>
                </td>
            </tr>
        `).join('');
        
    } catch (error) {
        console.error('Error al cargar productos:', error);
        mostrarAlerta('Error al cargar productos', 'danger');
    }
}

// Filtrar tabla en tiempo real
function filtrarTabla() {
    const buscar = document.getElementById('filtroBuscar').value.toLowerCase();
    const filas = document.querySelectorAll('#tablaProductos tr');
    
    filas.forEach(fila => {
        const codigo = fila.getAttribute('data-codigo') || '';
        const nombre = fila.getAttribute('data-nombre') || '';
        
        if (codigo.toLowerCase().includes(buscar) || nombre.includes(buscar)) {
            fila.style.display = '';
        } else {
            fila.style.display = 'none';
        }
    });
}

// Abrir modal para nuevo producto
function abrirModalNuevoProducto() {
    modoEdicion = false;
    document.getElementById('modalTitulo').textContent = 'Nuevo Producto/Servicio';
    document.getElementById('formProducto').reset();
    document.getElementById('productoId').value = '';
    document.getElementById('codigo').disabled = false;
    document.getElementById('activo').value = '1';
    document.getElementById('modalProducto').classList.add('show');
}

// Editar producto
async function editarProducto(id) {
    try {
        const response = await fetch(`/api/productos/${id}`);
        const producto = await response.json();
        
        modoEdicion = true;
        document.getElementById('modalTitulo').textContent = 'Editar Producto/Servicio';
        document.getElementById('productoId').value = producto.id;
        document.getElementById('codigo').value = producto.codigo;
        document.getElementById('codigo').disabled = true;
        document.getElementById('nombre').value = producto.nombre;
        document.getElementById('descripcion').value = producto.descripcion || '';
        document.getElementById('tipo').value = producto.tipo;
        document.getElementById('precio').value = producto.precio;
        document.getElementById('unidad').value = producto.unidad;
        document.getElementById('categoria').value = producto.categoria || '';
        document.getElementById('activo').value = producto.activo;
        document.getElementById('modalProducto').classList.add('show');
        
    } catch (error) {
        console.error('Error al cargar producto:', error);
        mostrarAlerta('Error al cargar producto', 'danger');
    }
}

// Guardar producto (crear o actualizar)
async function guardarProducto(e) {
    e.preventDefault();
    
    const id = document.getElementById('productoId').value;
    const codigo = document.getElementById('codigo').value;
    const nombre = document.getElementById('nombre').value;
    const descripcion = document.getElementById('descripcion').value;
    const tipo = document.getElementById('tipo').value;
    const precio = parseFloat(document.getElementById('precio').value);
    const unidad = document.getElementById('unidad').value;
    const categoria = document.getElementById('categoria').value;
    const activo = parseInt(document.getElementById('activo').value);
    
    try {
        if (modoEdicion) {
            // Actualizar producto existente
            const response = await fetch(`/api/productos/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    codigo: codigo,
                    nombre: nombre,
                    descripcion: descripcion,
                    tipo: tipo,
                    precio: precio,
                    unidad: unidad,
                    categoria: categoria,
                    activo: activo
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                mostrarAlerta('Producto actualizado exitosamente', 'success');
                cerrarModal();
                cargarCategorias();
                cargarProductos();
            } else {
                mostrarAlerta(data.message || 'Error al actualizar producto', 'danger');
            }
            
        } else {
            // Crear nuevo producto
            const response = await fetch('/api/productos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    codigo: codigo,
                    nombre: nombre,
                    descripcion: descripcion,
                    tipo: tipo,
                    precio: precio,
                    unidad: unidad,
                    categoria: categoria
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                mostrarAlerta('Producto creado exitosamente', 'success');
                cerrarModal();
                cargarCategorias();
                cargarProductos();
            } else {
                mostrarAlerta(data.message || 'Error al crear producto', 'danger');
            }
        }
        
    } catch (error) {
        console.error('Error al guardar producto:', error);
        mostrarAlerta('Error al guardar producto', 'danger');
    }
}

// Eliminar producto
async function eliminarProducto(id) {
    if (!confirm('¿Estás seguro de que deseas eliminar este producto?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/productos/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            mostrarAlerta('Producto eliminado exitosamente', 'success');
            cargarCategorias();
            cargarProductos();
        } else {
            mostrarAlerta(data.message || 'Error al eliminar producto', 'danger');
        }
        
    } catch (error) {
        console.error('Error al eliminar producto:', error);
        mostrarAlerta('Error al eliminar producto', 'danger');
    }
}

// Cerrar modal
function cerrarModal() {
    document.getElementById('modalProducto').classList.remove('show');
}

// Cerrar modal al hacer clic fuera
document.addEventListener('click', function(e) {
    const modal = document.getElementById('modalProducto');
    if (e.target === modal) {
        cerrarModal();
    }
});

// Mostrar alertas
function mostrarAlerta(mensaje, tipo = 'success') {
    const alert = document.getElementById('alert');
    alert.textContent = mensaje;
    alert.className = `alert alert-${tipo} show`;
    
    setTimeout(() => {
        alert.classList.remove('show');
    }, 5000);
}

// Formatear precio
function formatearPrecio(precio) {
    return new Intl.NumberFormat('es-MX', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(precio);
}
