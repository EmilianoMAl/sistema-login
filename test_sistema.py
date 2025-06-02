#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pruebas del Sistema de Login Local
=================================

Script de pruebas para verificar el correcto funcionamiento
del sistema de autenticación.
"""

import os
import json
import tempfile
from auth_system import AuthSystem


def test_hash_password():
    """Prueba el cifrado de contraseñas."""
    print("🧪 Probando cifrado de contraseñas...")

    # Crear sistema temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    # Probar cifrado
    password = "mi_contraseña_secreta"
    hashed1 = auth._hash_password(password)
    hashed2 = auth._hash_password(password)

    # Las mismas contraseñas deben generar el mismo hash
    assert hashed1 == hashed2, "❌ El hash debe ser consistente"

    # El hash debe ser diferente a la contraseña original
    assert hashed1 != password, "❌ El hash debe ser diferente a la contraseña"

    # El hash debe tener longitud esperada (SHA-256 = 64 caracteres hex)
    assert len(
        hashed1) == 64, f"❌ Hash debe tener 64 caracteres, tiene {len(hashed1)}"

    print("✅ Cifrado de contraseñas funciona correctamente")

    # Limpiar
    os.unlink(temp_file)


def test_register_user():
    """Prueba el registro de usuarios."""
    print("🧪 Probando registro de usuarios...")

    # Crear sistema temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    # Registro exitoso
    success, message = auth.register_user("usuario_test", "contraseña123")
    assert success, f"❌ Registro debería ser exitoso: {message}"

    # Usuario duplicado
    success, message = auth.register_user("usuario_test", "otra_contraseña")
    assert not success, "❌ No debería permitir usuarios duplicados"

    # Validaciones
    success, message = auth.register_user("", "contraseña123")
    assert not success, "❌ No debería permitir usuario vacío"

    success, message = auth.register_user("usuario", "123")
    assert not success, "❌ No debería permitir contraseña muy corta"

    success, message = auth.register_user("ab", "contraseña123")
    assert not success, "❌ No debería permitir usuario muy corto"

    print("✅ Registro de usuarios funciona correctamente")

    # Limpiar
    os.unlink(temp_file)


def test_login():
    """Prueba el sistema de login."""
    print("🧪 Probando sistema de login...")

    # Crear sistema temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    # Registrar usuario de prueba
    auth.register_user("test_user", "password123")

    # Login exitoso
    success, message = auth.login("test_user", "password123")
    assert success, f"❌ Login debería ser exitoso: {message}"

    # Contraseña incorrecta
    success, message = auth.login("test_user", "password_incorrecta")
    assert not success, "❌ Login debería fallar con contraseña incorrecta"

    # Usuario inexistente
    success, message = auth.login("usuario_inexistente", "password123")
    assert not success, "❌ Login debería fallar con usuario inexistente"

    print("✅ Sistema de login funciona correctamente")

    # Limpiar
    os.unlink(temp_file)


def test_failed_attempts():
    """Prueba el control de intentos fallidos."""
    print("🧪 Probando control de intentos fallidos...")

    # Crear sistema temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    # Registrar usuario de prueba
    auth.register_user("test_user", "password123")

    # Hacer 3 intentos fallidos
    for i in range(3):
        success, message = auth.login("test_user", "password_incorrecta")
        assert not success, f"❌ Intento {i+1} debería fallar"

    # El cuarto intento debería estar bloqueado
    # Incluso con contraseña correcta
    success, message = auth.login("test_user", "password123")
    assert not success, "❌ Usuario debería estar bloqueado después de 3 intentos"
    assert "bloqueado" in message.lower(), "❌ Mensaje debería indicar bloqueo"

    print("✅ Control de intentos fallidos funciona correctamente")

    # Limpiar
    os.unlink(temp_file)


def test_file_operations():
    """Prueba las operaciones de archivo."""
    print("🧪 Probando operaciones de archivo...")

    # Crear sistema temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    # Registrar algunos usuarios
    auth.register_user("user1", "password1")
    auth.register_user("user2", "password2")

    # Verificar que el archivo existe y tiene contenido válido
    assert os.path.exists(temp_file), "❌ Archivo de usuarios debería existir"

    with open(temp_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)

    assert "user1" in users_data, "❌ user1 debería estar en el archivo"
    assert "user2" in users_data, "❌ user2 debería estar en el archivo"
    assert "password" in users_data["user1"], "❌ user1 debería tener campo password"
    assert "created_at" in users_data["user1"], "❌ user1 debería tener campo created_at"

    # Verificar que las contraseñas están cifradas
    assert users_data["user1"]["password"] != "password1", "❌ Contraseña debería estar cifrada"

    print("✅ Operaciones de archivo funcionan correctamente")

    # Limpiar
    os.unlink(temp_file)


def test_user_utilities():
    """Prueba las utilidades de usuario."""
    print("🧪 Probando utilidades de usuario...")

    # Crear sistema temporal
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    # Verificar conteo inicial
    assert auth.get_user_count() == 0, "❌ Conteo inicial debería ser 0"

    # Agregar usuarios
    auth.register_user("user1", "password1")
    assert auth.get_user_count() == 1, "❌ Conteo debería ser 1"
    assert auth.user_exists("user1"), "❌ user1 debería existir"
    assert not auth.user_exists(
        "user_inexistente"), "❌ usuario inexistente no debería existir"

    auth.register_user("user2", "password2")
    assert auth.get_user_count() == 2, "❌ Conteo debería ser 2"

    print("✅ Utilidades de usuario funcionan correctamente")

    # Limpiar
    os.unlink(temp_file)


def run_all_tests():
    """Ejecuta todas las pruebas."""
    print("🚀 Iniciando pruebas del Sistema de Login Local...")
    print("=" * 60)

    try:
        test_hash_password()
        test_register_user()
        test_login()
        test_failed_attempts()
        test_file_operations()
        test_user_utilities()

        print("=" * 60)
        print("🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("✅ El sistema está funcionando correctamente")

    except AssertionError as e:
        print(f"❌ Error en las pruebas: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

    return True


def demo_system():
    """Demostración del sistema con usuarios de ejemplo."""
    print("\n" + "=" * 60)
    print("🎭 DEMOSTRACIÓN DEL SISTEMA")
    print("=" * 60)

    # Crear sistema temporal para demo
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name

    auth = AuthSystem(temp_file)

    print("📝 Registrando usuarios de ejemplo...")

    # Registrar usuarios de ejemplo
    users_demo = [
        ("admin", "admin123"),
        ("usuario1", "password123"),
        ("juan_perez", "miclave456")
    ]

    for username, password in users_demo:
        success, message = auth.register_user(username, password)
        if success:
            print(f"✅ {username}: {message}")
        else:
            print(f"❌ {username}: {message}")

    print(f"\n📊 Total de usuarios registrados: {auth.get_user_count()}")

    print("\n🔐 Probando login exitoso...")
    success, message = auth.login("admin", "admin123")
    print(f"Login admin: {'✅' if success else '❌'} {message}")

    print("\n🚫 Probando login fallido...")
    success, message = auth.login("admin", "password_incorrecta")
    print(f"Login fallido: {'✅' if not success else '❌'} {message}")

    print("\n📄 Contenido del archivo users.json:")
    with open(temp_file, 'r', encoding='utf-8') as f:
        users_data = json.load(f)

    for username, data in users_data.items():
        created_at = data["created_at"][:19].replace('T', ' ')
        print(f"  👤 {username} - Registrado: {created_at}")

    # Limpiar
    os.unlink(temp_file)

    print("\n🎉 ¡Demostración completada!")


if __name__ == "__main__":
    # Ejecutar pruebas
    if run_all_tests():
        # Si las pruebas pasan, mostrar demostración
        demo_system()
    else:
        print("❌ Las pruebas fallaron. Revisa el código.")
        exit(1)
