import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('cotizaciones.db')
cursor = conn.cursor()

# Eliminar todos los items de cotizaciones
cursor.execute('DELETE FROM cotizacion_items')
print('✓ Items de cotizaciones eliminados')

# Eliminar todas las cotizaciones
cursor.execute('DELETE FROM cotizaciones')
print('✓ Cotizaciones eliminadas')

# Reiniciar el autoincrement
cursor.execute('DELETE FROM sqlite_sequence WHERE name="cotizaciones"')
cursor.execute('DELETE FROM sqlite_sequence WHERE name="cotizacion_items"')
print('✓ Contadores reiniciados')

conn.commit()

# Verificar
cursor.execute('SELECT COUNT(*) FROM cotizaciones')
count = cursor.fetchone()[0]
print(f'\nTotal de cotizaciones en la base de datos: {count}')

conn.close()
print('\n✓ Base de datos limpia y lista para pruebas')
