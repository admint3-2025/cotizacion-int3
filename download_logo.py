"""
Script para descargar y guardar el logo localmente
"""
import urllib.request
import os

logo_url = "https://integrational3.com.mx/logorigen/integrational_std2.png"
logo_path = "static/images/logo_integrational3.png"

print("Descargando logo de Integrational3...")

try:
    # Agregar User-Agent para evitar bloqueos
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(logo_url, headers=headers)
    
    with urllib.request.urlopen(req, timeout=10) as response:
        logo_data = response.read()
        
        # Guardar el logo
        with open(logo_path, 'wb') as f:
            f.write(logo_data)
        
        print(f"✓ Logo guardado exitosamente en: {logo_path}")
        print(f"  Tamaño: {len(logo_data)} bytes")
        
except Exception as e:
    print(f"✗ Error al descargar el logo: {e}")
    print("\nCreando logo de respaldo...")
    
    # Si falla, crear un logo de texto simple
    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from PIL import Image, ImageDraw, ImageFont
    
    # Crear imagen con PIL
    img = Image.new('RGB', (800, 200), color=(26, 84, 144))  # Azul corporativo
    d = ImageDraw.Draw(img)
    
    try:
        # Intentar usar una fuente grande
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    # Dibujar el texto
    text = "Integrational 3"
    d.text((50, 70), text, fill=(255, 255, 255), font=font)
    
    # Guardar la imagen
    img.save(logo_path, 'PNG')
    print(f"✓ Logo de respaldo creado en: {logo_path}")

print("\nListo para usar en PDFs!")
