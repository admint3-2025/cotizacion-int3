"""
Script para generar una cotización de prueba con el nuevo formato
"""
from pdf_generator import PDFGenerator
from datetime import datetime

# Datos de prueba similares a la imagen
cotizacion_test = {
    'numero_cotizacion': 'INT-20251203-4891',
    'nombre': 'Grupo Alzen',
    'direccion': 'AVANZA ASESORIA PROFESIONAL',
    'email': 'reykofire@gmail.com',
    'telefono': '3338986000',
    'fecha_creacion': '2025-12-03 00:00:00',
    'fecha_validez': '2025-03-12',
    'subtotal': 2158.36,
    'iva': 345.34,
    'total': 2503.70,
    'notas': '',
    'items': [
        {
            'concepto': 'SIGA-HFD',
            'descripcion': 'INTELLIGENT FIXED TEMPERATURE DETECTOR',
            'cantidad': 1,
            'precio_unitario': 2158.36,
            'subtotal': 2158.36
        }
    ]
}

print("=" * 60)
print("GENERANDO PDF DE PRUEBA CON NUEVO FORMATO")
print("=" * 60)

try:
    pdf_gen = PDFGenerator()
    pdf_path = pdf_gen.generar_cotizacion_pdf(cotizacion_test, 'PRUEBA_INT-20251203-4891.pdf')
    print(f"\n✓ PDF generado exitosamente")
    print(f"  Ruta: {pdf_path}")
    print(f"\n📄 Abre el archivo para ver el nuevo formato:")
    print(f"   {pdf_path}")
except Exception as e:
    print(f"\n✗ Error al generar PDF: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
