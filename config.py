import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración de la aplicación"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Base de datos
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'cotizaciones.db')
    
    # SMTP - Configuración de correo
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_EMAIL = os.getenv('SMTP_EMAIL', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    # URL base del sistema (para enlaces de aprobación)
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # Directorios
    PDF_FOLDER = 'pdfs'
    UPLOAD_FOLDER = 'uploads'
    
    # Configuración de la empresa (personalizable)
    EMPRESA_NOMBRE = 'Integrational3'
    EMPRESA_SLOGAN = 'Soluciones Tecnológicas Integrales'
    EMPRESA_DIRECCION = 'Aguascalientes, México'
    EMPRESA_TELEFONO = '449 356 6356'
    EMPRESA_EMAIL = 'proyectos@integrational3.com.mx'
    EMPRESA_SITIO_WEB = 'www.integrational3.com.mx'
    EMPRESA_LOGO_URL = 'https://integrational3.com.mx/logorigen/integrational_std2.png'
