#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la configuración de zona horaria
"""

from datetime import datetime
import pytz

# Zona horaria de México
tz_mexico = pytz.timezone('America/Mexico_City')

# Hora actual del servidor (probablemente UTC en producción)
hora_servidor = datetime.now()
print(f"Hora del servidor (sin timezone): {hora_servidor}")
print(f"Formato: {hora_servidor.strftime('%d/%m/%Y %H:%M:%S')}")
print()

# Hora actual en México
hora_mexico = datetime.now(tz_mexico)
print(f"Hora en México (America/Mexico_City): {hora_mexico}")
print(f"Formato: {hora_mexico.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Timezone: {hora_mexico.tzinfo}")
print()

# Diferencia
if hora_servidor.tzinfo is None:
    print("⚠️ hora_servidor no tiene timezone (naive datetime)")
    print("En producción, si el servidor está en UTC, habrá diferencia de 6 horas")
else:
    diferencia = (hora_servidor - hora_mexico).total_seconds() / 3600
    print(f"Diferencia: {diferencia} horas")

print()
print("✓ pytz instalado correctamente")
print("✓ Zona horaria America/Mexico_City disponible")
