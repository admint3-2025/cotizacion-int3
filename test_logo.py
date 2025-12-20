"""
Script de prueba rápida del logo
"""
import urllib.request
from io import BytesIO
from config import Config

print("=" * 60)
print("PRUEBA DE DESCARGA DEL LOGO")
print("=" * 60)
print(f"\nURL del logo: {Config.EMPRESA_LOGO_URL}")
print("\nIntentando descargar...")

try:
    with urllib.request.urlopen(Config.EMPRESA_LOGO_URL) as response:
        logo_data = response.read()
        print(f"✓ Logo descargado exitosamente")
        print(f"  Tamaño: {len(logo_data)} bytes")
        print(f"  Tipo de contenido: {response.headers.get('Content-Type')}")
        print("\n✓ El logo está listo para usarse en PDFs y emails")
except Exception as e:
    print(f"✗ Error al descargar el logo: {e}")

print("\nDatos de la empresa:")
print(f"  Nombre: {Config.EMPRESA_NOMBRE}")
print(f"  Slogan: {Config.EMPRESA_SLOGAN}")
print(f"  Dirección: {Config.EMPRESA_DIRECCION}")
print(f"  Teléfono: {Config.EMPRESA_TELEFONO}")
print(f"  Email: {Config.EMPRESA_EMAIL}")
print(f"  Sitio web: {Config.EMPRESA_SITIO_WEB}")
print("=" * 60)
