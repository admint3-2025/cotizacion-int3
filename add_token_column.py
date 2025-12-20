import sqlite3
import secrets

# Conectar a la base de datos
conn = sqlite3.connect('cotizaciones.db')
cursor = conn.cursor()

# Agregar la columna token_aprobacion (sin UNIQUE porque SQLite no lo permite en ALTER)
try:
    cursor.execute('ALTER TABLE cotizaciones ADD COLUMN token_aprobacion TEXT')
    conn.commit()
    print('✓ Columna token_aprobacion agregada')
except sqlite3.OperationalError as e:
    print(f'Columna ya existe o error: {e}')

# Generar tokens para todas las cotizaciones existentes sin token
cursor.execute('SELECT id FROM cotizaciones WHERE token_aprobacion IS NULL')
rows = cursor.fetchall()

if rows:
    print(f'\nGenerando tokens para {len(rows)} cotizaciones...')
    for row in rows:
        token = secrets.token_urlsafe(32)
        cursor.execute('UPDATE cotizaciones SET token_aprobacion = ? WHERE id = ?', (token, row[0]))
    conn.commit()
    print(f'✓ {len(rows)} tokens generados exitosamente')
else:
    print('Todas las cotizaciones ya tienen token')

# Verificar
cursor.execute('SELECT id, numero_cotizacion, token_aprobacion FROM cotizaciones')
cotizaciones = cursor.fetchall()
print(f'\n=== VERIFICACIÓN ===')
for cot in cotizaciones:
    token_preview = cot[2][:20] + '...' if cot[2] else 'NULL'
    print(f'ID {cot[0]}: {cot[1]} - Token: {token_preview}')

conn.close()
print('\n✓ Proceso completado')
