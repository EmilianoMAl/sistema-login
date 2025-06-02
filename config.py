#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuración del Sistema de Login Local
========================================

Archivo de configuración que permite personalizar el comportamiento
del sistema de autenticación.
"""

# Configuración de Seguridad
SECURITY_CONFIG = {
    # Número máximo de intentos fallidos antes del bloqueo
    "max_failed_attempts": 3,

    # Longitud mínima del nombre de usuario
    "min_username_length": 3,

    # Longitud máxima del nombre de usuario
    "max_username_length": 30,

    # Longitud mínima de la contraseña
    "min_password_length": 6,

    # Longitud máxima de la contraseña
    "max_password_length": 100,

    # Algoritmo de hash para contraseñas
    "hash_algorithm": "sha256",

    # Caracteres permitidos en nombres de usuario (regex)
    "username_pattern": r"^[a-zA-Z0-9_.-]+$",
}

# Configuración de Archivos
FILE_CONFIG = {
    # Nombre del archivo de usuarios
    "users_file": "users.json",

    # Codificación del archivo
    "file_encoding": "utf-8",

    # Indentación del JSON (para legibilidad)
    "json_indent": 4,

    # Crear backup automático
    "auto_backup": False,

    # Carpeta de backups
    "backup_folder": "backups",
}

# Configuración de Interfaz
UI_CONFIG = {
    # Usar colores en la consola (si está disponible)
    "use_colors": True,

    # Usar emojis en la interfaz
    "use_emojis": True,

    # Limpiar pantalla automáticamente
    "auto_clear_screen": True,

    # Ancho de los separadores
    "separator_width": 60,

    # Tiempo de espera para mensajes (segundos)
    "message_delay": 0,
}

# Configuración de Validación
VALIDATION_CONFIG = {
    # Validar que las contraseñas no sean comunes
    "check_common_passwords": False,

    # Lista de contraseñas comunes a evitar
    "common_passwords": [
        "123456", "password", "admin", "qwerty",
        "letmein", "welcome", "monkey", "dragon"
    ],

    # Requerir al menos un número en la contraseña
    "require_number": False,

    # Requerir al menos una letra mayúscula
    "require_uppercase": False,

    # Requerir al menos un símbolo especial
    "require_special_char": False,

    # Símbolos especiales permitidos
    "special_chars": "!@#$%^&*()_+-=[]{}|;:,.<>?",
}

# Configuración de Logging (para futuras implementaciones)
LOGGING_CONFIG = {
    # Habilitar logging
    "enable_logging": False,

    # Archivo de logs
    "log_file": "login_system.log",

    # Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    "log_level": "INFO",

    # Rotar logs automáticamente
    "log_rotation": True,

    # Tamaño máximo del archivo de log (MB)
    "max_log_size_mb": 10,

    # Número máximo de archivos de log a mantener
    "max_log_files": 5,
}

# Configuración de Desarrollo
DEV_CONFIG = {
    # Modo debug (muestra información adicional)
    "debug_mode": False,

    # Mostrar tiempo de ejecución de operaciones
    "show_timing": False,

    # Mostrar información detallada de errores
    "verbose_errors": False,
}


def get_config_value(category: str, key: str, default=None):
    """
    Obtiene un valor de configuración específico.

    Args:
        category (str): Categoría de configuración
        key (str): Clave de configuración
        default: Valor por defecto si no se encuentra

    Returns:
        Valor de configuración o valor por defecto
    """
    configs = {
        'security': SECURITY_CONFIG,
        'file': FILE_CONFIG,
        'ui': UI_CONFIG,
        'validation': VALIDATION_CONFIG,
        'logging': LOGGING_CONFIG,
        'dev': DEV_CONFIG,
    }

    category_config = configs.get(category.lower(), {})
    return category_config.get(key, default)


def validate_config():
    """
    Valida que la configuración sea coherente.

    Returns:
        Tuple[bool, str]: (es_válida, mensaje_error)
    """
    errors = []

    # Validar configuración de seguridad
    if SECURITY_CONFIG['max_failed_attempts'] < 1:
        errors.append("max_failed_attempts debe ser mayor a 0")

    if SECURITY_CONFIG['min_username_length'] < 1:
        errors.append("min_username_length debe ser mayor a 0")

    if SECURITY_CONFIG['min_password_length'] < 1:
        errors.append("min_password_length debe ser mayor a 0")

    if SECURITY_CONFIG['min_username_length'] > SECURITY_CONFIG['max_username_length']:
        errors.append(
            "min_username_length no puede ser mayor que max_username_length")

    if SECURITY_CONFIG['min_password_length'] > SECURITY_CONFIG['max_password_length']:
        errors.append(
            "min_password_length no puede ser mayor que max_password_length")

    # Validar configuración de archivos
    if not FILE_CONFIG['users_file']:
        errors.append("users_file no puede estar vacío")

    if FILE_CONFIG['json_indent'] < 0:
        errors.append("json_indent debe ser mayor o igual a 0")

    if errors:
        return False, "; ".join(errors)

    return True, "Configuración válida"


def print_config():
    """
    Imprime la configuración actual del sistema.
    """
    print("=" * 60)
    print("CONFIGURACIÓN DEL SISTEMA DE LOGIN")
    print("=" * 60)

    configs = [
        ("🔒 SEGURIDAD", SECURITY_CONFIG),
        ("📁 ARCHIVOS", FILE_CONFIG),
        ("🖥️  INTERFAZ", UI_CONFIG),
        ("✅ VALIDACIÓN", VALIDATION_CONFIG),
        ("📝 LOGGING", LOGGING_CONFIG),
        ("🔧 DESARROLLO", DEV_CONFIG),
    ]

    for title, config in configs:
        print(f"\n{title}:")
        for key, value in config.items():
            print(f"  {key}: {value}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Mostrar configuración y validarla
    print_config()

    is_valid, message = validate_config()
    print(f"\n{'✅' if is_valid else '❌'} {message}")
