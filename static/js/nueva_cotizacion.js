// Funciones necesarias para nueva cotización
let productos = [];
let itemCounter = 0;
let inactividadTimer = null;
const TIEMPO_INACTIVIDAD = 5 * 60 * 1000; // 5 minutos

// Inicialización
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/session');
        const data = await response.json();
        
        if (!data.authenticated) {
            window.location.href = '/login';
            return;
        }
        
        // Actualizar nombre de usuario
        document.getElementById('nombreUsuario').textContent = data.usuario.nombre_completo;
        
        // Cargar datos
        await cargarProductos();
        await cargarClientesSelect();
        
        // Event listeners
        document.getElementById('cotizacion-form').addEventListener('submit', crearCotizacion);
        const formProdRapido = document.getElementById('productoRapidoForm');
        if (formProdRapido) {
            formProdRapido.addEventListener('submit', crearProductoRapido);
        }
        
        // Agregar item inicial
        agregarItem();
        
        // Iniciar temporizador de inactividad
        iniciarTemporizadorInactividad();
    } catch (error) {
        console.error('Error:', error);
        window.location.href = '/login';
    }
});

// Temporizador de inactividad
function iniciarTemporizadorInactividad() {
    const eventos = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    eventos.forEach(evento => {
        document.addEventListener(evento, resetearTemporizador, true);
    });
    resetearTemporizador();
}

function resetearTemporizador() {
    if (inactividadTimer) {
        clearTimeout(inactividadTimer);
    }
    inactividadTimer = setTimeout(async () => {
        alert('Sesión cerrada por inactividad');
        try {
            await fetch('/api/logout', { method: 'POST' });
        } catch (error) {
            console.error('Error:', error);
        }
        window.location.href = '/login';
    }, TIEMPO_INACTIVIDAD);
}

async function cargarProductos() {
    try {
        const response = await fetch('/api/productos');
        productos = await response.json();
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

async function cargarClientesSelect() {
    try {
        const response = await fetch('/api/clientes');
        const clientes = await response.json();
        
        const select = document.getElementById('cotizacion-cliente');
        select.innerHTML = '<option value="">Seleccione un cliente...</option>';
        
        clientes.forEach(cliente => {
            const option = document.createElement('option');
            option.value = cliente.id;
            option.textContent = cliente.nombre;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar clientes:', error);
    }
}

function agregarItem() {
    itemCounter++;
    const container = document.getElementById('items-container');
    
    const itemDiv = document.createElement('div');
    itemDiv.className = 'item-row';
    itemDiv.id = `item-${itemCounter}`;
    itemDiv.innerHTML = `
        <div class="item-grid">
            <div class="form-group">
                <label>Producto/Servicio</label>
                <select class="item-producto" onchange="actualizarPrecioItem(${itemCounter})">
                    <option value="">Seleccione...</option>
                    ${productos.map(p => `<option value="${p.id}" data-precio="${p.precio}">${p.nombre}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Descripción</label>
                <input type="text" class="item-descripcion" placeholder="Descripción detallada">
            </div>
            <div class="form-group">
                <label>Cantidad</label>
                <input type="number" class="item-cantidad" value="1" min="0" oninput="calcularTotales()">
            </div>
            <div class="form-group">
                <label>Precio Unitario</label>
                <input type="number" class="item-precio" step="0.01" min="0" oninput="calcularTotales()">
            </div>
            <div class="form-group">
                <button type="button" class="btn btn-success" onclick="abrirModalProductoRapido(${itemCounter})" style="white-space: nowrap;">Nuevo</button>
            </div>
            <div class="form-group">
                <button type="button" class="btn btn-danger btn-sm" onclick="eliminarItem(${itemCounter})">Eliminar</button>
            </div>
        </div>
    `;
    
    container.appendChild(itemDiv);
    calcularTotales();
}

function eliminarItem(itemId) {
    const item = document.getElementById(`item-${itemId}`);
    if (item) {
        item.remove();
        calcularTotales();
    }
}

function actualizarPrecioItem(itemId) {
    const itemDiv = document.getElementById(`item-${itemId}`);
    const select = itemDiv.querySelector('.item-producto');
    const selectedOption = select.options[select.selectedIndex];
    const precio = selectedOption.getAttribute('data-precio');
    
    if (precio) {
        itemDiv.querySelector('.item-precio').value = precio;
        
        const productoId = select.value;
        const producto = productos.find(p => p.id == productoId);
        if (producto && producto.descripcion) {
            itemDiv.querySelector('.item-descripcion').value = producto.descripcion;
        }
    }
    
    calcularTotales();
}

function calcularTotales() {
    const items = document.querySelectorAll('.item-row');
    let subtotal = 0;
    
    items.forEach(item => {
        const cantidad = parseFloat(item.querySelector('.item-cantidad').value) || 0;
        const precio = parseFloat(item.querySelector('.item-precio').value) || 0;
        subtotal += cantidad * precio;
    });
    
    const iva = subtotal * 0.16;
    const total = subtotal + iva;
    
    document.getElementById('subtotal-display').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('iva-display').textContent = `$${iva.toFixed(2)}`;
    document.getElementById('total-display').textContent = `$${total.toFixed(2)}`;
}

async function crearCotizacion(e) {
    e.preventDefault();
    
    const items = [];
    document.querySelectorAll('.item-row').forEach(itemDiv => {
        const productoSelect = itemDiv.querySelector('.item-producto');
        const cantidad = parseFloat(itemDiv.querySelector('.item-cantidad').value) || 0;
        const precio = parseFloat(itemDiv.querySelector('.item-precio').value) || 0;
        
        if (cantidad > 0 && precio >= 0) {
            items.push({
                producto_id: productoSelect.value || null,
                concepto: productoSelect.options[productoSelect.selectedIndex].text,
                descripcion: itemDiv.querySelector('.item-descripcion').value,
                cantidad: cantidad,
                precio_unitario: precio
            });
        }
    });
    
    if (items.length === 0) {
        alert('Debe agregar al menos un concepto');
        return;
    }
    
    const data = {
        cliente_id: document.getElementById('cotizacion-cliente').value,
        fecha_validez: document.getElementById('cotizacion-validez').value,
        items: items,
        notas: document.getElementById('cotizacion-notas').value,
        condiciones_comerciales: document.getElementById('cotizacion-condiciones').value
    };
    
    try {
        const response = await fetch('/api/cotizaciones', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Cotización creada exitosamente');
            // Opcional: cerrar ventana
            setTimeout(() => window.close(), 1000);
        } else {
            const error = await response.json();
            alert('Error: ' + (error.message || 'Error al crear cotización'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear cotización');
    }
}

function abrirModalProductoRapido(itemId) {
    document.getElementById('itemIndexProducto').value = itemId;
    document.getElementById('modalProductoRapido').style.display = 'flex';
}

function cerrarModalProductoRapido() {
    document.getElementById('modalProductoRapido').style.display = 'none';
    document.getElementById('productoRapidoForm').reset();
}

async function crearProductoRapido(e) {
    e.preventDefault();
    
    const data = {
        nombre: document.getElementById('productoRapidoNombre').value,
        descripcion: document.getElementById('productoRapidoDescripcion').value,
        precio: parseFloat(document.getElementById('productoRapidoPrecio').value),
        categoria: document.getElementById('productoRapidoCategoria').value
    };
    
    try {
        const response = await fetch('/api/productos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            await cargarProductos();
            
            const itemId = document.getElementById('itemIndexProducto').value;
            const itemDiv = document.getElementById(`item-${itemId}`);
            const select = itemDiv.querySelector('.item-producto');
            
            const nuevoProducto = productos[productos.length - 1];
            const option = document.createElement('option');
            option.value = nuevoProducto.id;
            option.setAttribute('data-precio', nuevoProducto.precio);
            option.textContent = nuevoProducto.nombre;
            option.selected = true;
            select.appendChild(option);
            
            actualizarPrecioItem(itemId);
            cerrarModalProductoRapido();
            alert('Producto creado exitosamente');
        } else {
            alert('Error al crear producto');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al crear producto');
    }
}
