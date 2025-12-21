import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('cotizaciones.db')
cursor = conn.cursor()

# Agregar columna emails_destino para guardar los emails a los que se envió
try:
    cursor.execute('ALTER TABLE cotizaciones ADD COLUMN emails_destino TEXT')
    conn.commit()
    print('✓ Columna emails_destino agregada')
except sqlite3.OperationalError as e:
    print(f'Columna ya existe o error: {e}')

conn.close()
print('✓ Proceso completado')
