"""
Script para insertar productos iniciales en la base de datos
Ejecutar en PythonAnywhere después de clonar el repositorio
"""
from database import Database

def insertar_productos_iniciales():
    db = Database()
    
    productos = [
        {
            'nombre': 'DETECTOR DE TEMPERATURA INTELIGENTE',
            'descripcion': '',
            'precio': 1980.00,
            'categoria': 'SDI',
            'activo': True
        },
        {
            'nombre': 'DETECTOR DE HUMO',
            'descripcion': 'DETECTORES DE HUMO',
            'precio': 1986.00,
            'categoria': 'SDI',
            'activo': True
        },
        {
            'nombre': 'Levantamiento de Campo y Creación de Base de Datos para Sistema de Incendio EDWARDS',
            'descripcion': 'Realizar el levantamiento físico, identificación, mapeo y digitalización de la base de datos de los dispositivos periféricos vinculados al panel de control de alarma de incendio existente (Marca EDWARDS, Serie EST3 o EST4 / iO Series según corresponda), con el fin de regularizar la matriz de señales y garantizar la correspondencia entre la ubicación física y la etiqueta lógica en el sistema.',
            'precio': 30000.00,
            'categoria': 'SDI',
            'activo': True
        },
        {
            'nombre': 'Servicio de Mantenimiento Preventivo Integral al Sistema de Detección y Alarma de Incendio',
            'descripcion': 'Consiste en la ejecución de pruebas funcionales, limpieza técnica y verificación de la integridad operativa de la plataforma de vida y seguridad marca EDWARDS. El objetivo es garantizar que todos los componentes (procesamiento, iniciación y notificación) respondan de acuerdo con las curvas de sensibilidad y tiempos de respuesta de fábrica, minimizando falsas alarmas y asegurando la activación en caso de emergencia.',
            'precio': 25000.00,
            'categoria': 'SDI',
            'activo': True
        },
        {
            'nombre': 'Servicio de Integración de Nuevos Dispositivos (Sin costo por un año)',
            'descripcion': 'Durante un periodo de 12 meses posteriores a la firma del contrato, los servicios de alta de dispositivos en el lazo (Loop), actualización de la base de datos del panel y mapeo de señales (Input/Output) se realizarán sin costo adicional. Esta condición aplica para cualquier dispositivo de iniciación o notificación suministrado por nuestra empresa, garantizando la expansión del sistema sin incrementar los costos de servicios de ingeniería.',
            'precio': 0.00,
            'categoria': 'SDI',
            'activo': True
        }
    ]
    
    print('Insertando productos iniciales...')
    for producto in productos:
        resultado = db.crear_producto(
            nombre=producto['nombre'],
            descripcion=producto['descripcion'],
            precio=producto['precio'],
            categoria=producto['categoria'],
            activo=producto['activo']
        )
        if resultado['success']:
            print(f"✓ {producto['nombre'][:50]}...")
        else:
            print(f"✗ Error: {resultado.get('message', 'Unknown error')}")
    
    print('\n¡Productos insertados correctamente!')

if __name__ == '__main__':
    insertar_productos_iniciales()
