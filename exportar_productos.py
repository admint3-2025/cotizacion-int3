import sqlite3
import json

# Conectar a la base de datos
conn = sqlite3.connect('cotizaciones.db')
cursor = conn.cursor()

# Obtener productos
cursor.execute('SELECT id, nombre, descripcion, precio, categoria FROM productos')
productos = cursor.fetchall()

print(f'Total productos: {len(productos)}\n')
print('Productos encontrados:')
print('='*80)

for p in productos:
    print(f'ID: {p[0]}')
    print(f'Nombre: {p[1]}')
    print(f'Descripción: {p[2]}')
    print(f'Precio: ${p[3]:,.2f}')
    print(f'Categoría: {p[4]}')
    print('-'*80)

conn.close()
