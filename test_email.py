"""
Script de prueba para verificar la configuración de email
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def test_email_connection():
    """Probar conexión al servidor SMTP"""
    
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    email = os.getenv('SMTP_EMAIL')
    password = os.getenv('SMTP_PASSWORD')
    
    print("=" * 60)
    print("PRUEBA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    print(f"\nServidor SMTP: {smtp_server}")
    print(f"Puerto: {smtp_port}")
    print(f"Usuario: {email}")
    print(f"Contraseña: {'*' * len(password) if password else 'NO CONFIGURADA'}")
    print()
    
    if not email or not password:
        print("❌ ERROR: Email o contraseña no configurados en .env")
        return False
    
    try:
        print("1. Conectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        print("   ✓ Conexión establecida")
        
        print("\n2. Iniciando TLS...")
        server.set_debuglevel(0)  # Cambiar a 1 para ver debug completo
        server.starttls()
        print("   ✓ TLS iniciado")
        
        print("\n3. Autenticando...")
        server.login(email, password)
        print("   ✓ Autenticación exitosa")
        
        print("\n4. Enviando email de prueba...")
        # Crear mensaje de prueba
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email  # Enviamos a nosotros mismos
        msg['Subject'] = "Prueba - Sistema de Cotización"
        
        body = """
        <html>
            <body>
                <h2>✓ Prueba Exitosa</h2>
                <p>La configuración de email está funcionando correctamente.</p>
                <p>El sistema de cotización puede enviar correos sin problemas.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        server.send_message(msg)
        print(f"   ✓ Email de prueba enviado a {email}")
        
        server.quit()
        print("\n" + "=" * 60)
        print("✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("=" * 60)
        print(f"\nRevisa tu bandeja de entrada en {email}")
        print("para confirmar la recepción del email de prueba.")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ ERROR DE AUTENTICACIÓN:")
        print(f"   {str(e)}")
        print("\nPosibles soluciones:")
        print("   - Verifica que el correo y contraseña sean correctos")
        print("   - Revisa que la contraseña no tenga espacios extra")
        print("   - Confirma que la cuenta esté activa")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ ERROR SMTP:")
        print(f"   {str(e)}")
        print("\nPosibles soluciones:")
        print("   - Verifica el servidor SMTP y el puerto")
        print("   - Asegúrate de tener conexión a internet")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL:")
        print(f"   {str(e)}")
        import traceback
        print("\nDetalle completo del error:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_email_connection()
