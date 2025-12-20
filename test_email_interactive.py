"""
Script interactivo para probar diferentes credenciales de email
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

def test_email_interactive():
    """Probar conexión al servidor SMTP con credenciales interactivas"""
    
    print("=" * 60)
    print("PRUEBA INTERACTIVA DE CONFIGURACIÓN DE EMAIL")
    print("=" * 60)
    
    # Solicitar configuración
    smtp_server = input("\nServidor SMTP [smtp.titan.email]: ").strip() or "smtp.titan.email"
    smtp_port = input("Puerto [587]: ").strip() or "587"
    smtp_port = int(smtp_port)
    email = input("Email: ").strip()
    
    print("\n⚠️  Ingresa la contraseña (no se mostrará en pantalla):")
    password = getpass.getpass("Contraseña: ")
    
    print(f"\n📧 Configuración:")
    print(f"   Servidor: {smtp_server}:{smtp_port}")
    print(f"   Email: {email}")
    print(f"   Contraseña: {'*' * len(password)}")
    
    confirmar = input("\n¿Continuar con estas credenciales? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Prueba cancelada.")
        return False
    
    try:
        print("\n1. Conectando al servidor SMTP...")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        print("   ✓ Conexión establecida")
        
        print("\n2. Iniciando TLS...")
        server.set_debuglevel(0)
        server.starttls()
        print("   ✓ TLS iniciado")
        
        print("\n3. Autenticando...")
        server.login(email, password)
        print("   ✓ Autenticación exitosa")
        
        print("\n4. Enviando email de prueba...")
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "✓ Prueba Exitosa - Sistema de Cotización"
        
        body = """
        <html>
            <body>
                <h2 style="color: green;">✓ Prueba Exitosa</h2>
                <p>La configuración de email está funcionando correctamente.</p>
                <p><strong>Servidor:</strong> """ + smtp_server + """</p>
                <p><strong>Puerto:</strong> """ + str(smtp_port) + """</p>
                <p>El sistema de cotización puede enviar correos sin problemas.</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        server.send_message(msg)
        print(f"   ✓ Email de prueba enviado a {email}")
        
        server.quit()
        print("\n" + "=" * 60)
        print("✓✓✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE ✓✓✓")
        print("=" * 60)
        print(f"\n📬 Revisa tu bandeja de entrada en {email}")
        print("\n💡 Ahora actualiza el archivo .env con estas credenciales:")
        print(f"\nSMTP_SERVER={smtp_server}")
        print(f"SMTP_PORT={smtp_port}")
        print(f"SMTP_EMAIL={email}")
        print(f"SMTP_PASSWORD={password}")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ ERROR DE AUTENTICACIÓN:")
        print(f"   {str(e)}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que el correo y contraseña sean correctos")
        print("   2. La contraseña puede contener caracteres especiales problemáticos")
        print("   3. Contacta a soporte de Titan para verificar:")
        print("      - Que el acceso SMTP esté habilitado")
        print("      - Si necesitas una 'contraseña de aplicación'")
        print("      - Si hay restricciones de IP o ubicación")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ ERROR SMTP:")
        print(f"   {str(e)}")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR GENERAL:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    while True:
        result = test_email_interactive()
        if result:
            break
        
        print("\n" + "=" * 60)
        reintentar = input("\n¿Deseas intentar con otras credenciales? (s/n): ").strip().lower()
        if reintentar != 's':
            break
    
    print("\n¡Hasta luego!")
