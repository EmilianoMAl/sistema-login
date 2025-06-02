#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Login Local - Archivo Principal
==========================================

Sistema de autenticación local con las siguientes características:
- Registro de usuarios con validación
- Login con control de intentos fallidos
- Contraseñas cifradas con SHA-256
- Almacenamiento en archivo JSON
- Interfaz de consola intuitiva

Autor: Sistema de Login
Versión: 1.0
"""

import os
import sys
from getpass import getpass
from auth_system import AuthSystem


class LoginInterface:
    """
    Interfaz de usuario para el sistema de login.
    """

    def __init__(self):
        """
        Inicializa la interfaz y el sistema de autenticación.
        """
        # Cambiar al directorio del script para que users.json se guarde en la misma carpeta
        script_dir = os.path.dirname(os.path.abspath(__file__))
        users_file = os.path.join(script_dir, "users.json")

        self.auth = AuthSystem(users_file)
        self.current_user = None

    def clear_screen(self):
        """
        Limpia la pantalla de la consola.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self, title: str):
        """
        Imprime un encabezado formateado.

        Args:
            title (str): Título a mostrar
        """
        print("=" * 60)
        print(f"{'':>20}{title:^20}{'':>20}")
        print("=" * 60)

    def print_separator(self):
        """
        Imprime una línea separadora.
        """
        print("-" * 60)

    def show_main_menu(self):
        """
        Muestra el menú principal del sistema.
        """
        self.clear_screen()
        self.print_header("SISTEMA DE LOGIN LOCAL")
        print()
        print("Selecciona una opción:")
        print()
        print("1. 👤 Registrar nuevo usuario")
        print("2. 🔐 Iniciar sesión")
        print("3. 📊 Mostrar estadísticas")
        print("4. ❌ Salir")
        print()
        self.print_separator()

    def show_user_menu(self):
        """
        Muestra el menú para usuarios autenticados.
        """
        self.clear_screen()
        self.print_header(f"BIENVENIDO, {self.current_user.upper()}")
        print()
        print("¡Has iniciado sesión exitosamente!")
        print()
        print("Opciones disponibles:")
        print()
        print("1. 📋 Ver información de la cuenta")
        print("2. 🔄 Cambiar usuario")
        print("3. 📊 Ver estadísticas del sistema")
        print("4. 🚪 Cerrar sesión")
        print()
        self.print_separator()

    def get_user_input(self, prompt: str, max_length: int = 50) -> str:
        """
        Obtiene entrada del usuario con validación básica.

        Args:
            prompt (str): Mensaje a mostrar
            max_length (int): Longitud máxima permitida

        Returns:
            str: Entrada del usuario limpia
        """
        while True:
            user_input = input(prompt).strip()
            if len(user_input) <= max_length:
                return user_input
            print(
                f"❌ La entrada es demasiado larga (máximo {max_length} caracteres)")

    def get_password_input(self, prompt: str = "Contraseña: ") -> str:
        """
        Obtiene una contraseña de forma segura (sin mostrarla en pantalla).

        Args:
            prompt (str): Mensaje a mostrar

        Returns:
            str: Contraseña ingresada
        """
        return getpass(prompt)

    def register_user(self):
        """
        Maneja el proceso de registro de un nuevo usuario.
        """
        self.clear_screen()
        self.print_header("REGISTRO DE NUEVO USUARIO")
        print()
        print("Complete la siguiente información:")
        print()

        # Obtener nombre de usuario
        username = self.get_user_input("👤 Nombre de usuario: ", 30)

        if not username:
            print("❌ El nombre de usuario no puede estar vacío")
            input("\nPresiona Enter para continuar...")
            return

        # Verificar si el usuario ya existe
        if self.auth.user_exists(username):
            print(f"❌ El usuario '{username}' ya existe")
            input("\nPresiona Enter para continuar...")
            return

        # Obtener contraseña
        print("\n🔐 Ingresa tu contraseña (mínimo 6 caracteres):")
        password = self.get_password_input()

        if not password:
            print("❌ La contraseña no puede estar vacía")
            input("\nPresiona Enter para continuar...")
            return

        # Confirmar contraseña
        confirm_password = self.get_password_input(
            "🔐 Confirma tu contraseña: ")

        if password != confirm_password:
            print("❌ Las contraseñas no coinciden")
            input("\nPresiona Enter para continuar...")
            return

        # Intentar registrar usuario
        success, message = self.auth.register_user(username, password)

        print()
        if success:
            print(f"✅ {message}")
            print(f"🎉 ¡Bienvenido al sistema, {username}!")
        else:
            print(f"❌ {message}")

        input("\nPresiona Enter para continuar...")

    def login_user(self):
        """
        Maneja el proceso de inicio de sesión.
        """
        self.clear_screen()
        self.print_header("INICIAR SESIÓN")
        print()

        # Obtener credenciales
        username = self.get_user_input("👤 Nombre de usuario: ", 30)

        if not username:
            print("❌ El nombre de usuario no puede estar vacío")
            input("\nPresiona Enter para continuar...")
            return

        password = self.get_password_input("🔐 Contraseña: ")

        if not password:
            print("❌ La contraseña no puede estar vacía")
            input("\nPresiona Enter para continuar...")
            return

        # Intentar login
        success, message = self.auth.login(username, password)

        print()
        if success:
            print(f"✅ {message}")
            self.current_user = username
            input("\nPresiona Enter para continuar...")
            self.user_session()
        else:
            print(f"❌ {message}")
            input("\nPresiona Enter para continuar...")

    def show_stats(self):
        """
        Muestra estadísticas del sistema.
        """
        self.clear_screen()
        self.print_header("ESTADÍSTICAS DEL SISTEMA")
        print()

        user_count = self.auth.get_user_count()

        print(f"📊 Total de usuarios registrados: {user_count}")

        if user_count == 0:
            print("📝 No hay usuarios registrados en el sistema")
        elif user_count == 1:
            print("👤 Hay 1 usuario registrado")
        else:
            print(f"👥 Hay {user_count} usuarios registrados")

        print()
        print("🔒 Sistema de seguridad:")
        print(f"   • Contraseñas cifradas con SHA-256")
        print(f"   • Máximo de intentos fallidos: {self.auth.max_attempts}")
        print(
            f"   • Archivo de datos: {os.path.basename(self.auth.users_file)}")

        print()
        input("Presiona Enter para continuar...")

    def show_account_info(self):
        """
        Muestra información de la cuenta del usuario actual.
        """
        self.clear_screen()
        self.print_header("INFORMACIÓN DE LA CUENTA")
        print()

        if self.current_user:
            print(f"👤 Usuario actual: {self.current_user}")
            print(f"✅ Estado: Sesión activa")
            print(f"🔐 Seguridad: Contraseña cifrada")

            # Información adicional
            users = self.auth._load_users()
            if self.current_user in users:
                user_data = users[self.current_user]
                if "created_at" in user_data:
                    created_at = user_data["created_at"][:19].replace('T', ' ')
                    print(f"📅 Fecha de registro: {created_at}")

        print()
        input("Presiona Enter para continuar...")

    def user_session(self):
        """
        Maneja la sesión de un usuario autenticado.
        """
        while True:
            self.show_user_menu()

            choice = input("Selecciona una opción (1-4): ").strip()

            if choice == "1":
                self.show_account_info()
            elif choice == "2":
                self.change_user()
                break
            elif choice == "3":
                self.show_stats()
            elif choice == "4":
                self.logout()
                break
            else:
                print("❌ Opción no válida. Por favor, selecciona 1, 2, 3 o 4.")
                input("Presiona Enter para continuar...")

    def change_user(self):
        """
        Permite cambiar de usuario sin cerrar el programa.
        """
        self.current_user = None
        print("🔄 Cambiando de usuario...")
        input("Presiona Enter para continuar...")

    def logout(self):
        """
        Cierra la sesión del usuario actual.
        """
        print(f"👋 ¡Hasta luego, {self.current_user}!")
        self.current_user = None
        input("Presiona Enter para continuar...")

    def run(self):
        """
        Ejecuta el bucle principal de la aplicación.
        """
        print("🚀 Iniciando Sistema de Login Local...")

        while True:
            if self.current_user:
                self.user_session()
            else:
                self.show_main_menu()

                choice = input("Selecciona una opción (1-4): ").strip()

                if choice == "1":
                    self.register_user()
                elif choice == "2":
                    self.login_user()
                elif choice == "3":
                    self.show_stats()
                elif choice == "4":
                    self.exit_program()
                    break
                else:
                    print("❌ Opción no válida. Por favor, selecciona 1, 2, 3 o 4.")
                    input("Presiona Enter para continuar...")

    def exit_program(self):
        """
        Termina el programa de forma elegante.
        """
        self.clear_screen()
        self.print_header("¡HASTA LUEGO!")
        print()
        print("Gracias por usar el Sistema de Login Local")
        print("🔒 Tus datos están seguros y cifrados")
        print()
        print("¡Que tengas un buen día! 👋")
        print()


def main():
    """
    Función principal del programa.
    """
    try:
        # Crear e iniciar la interfaz
        interface = LoginInterface()
        interface.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, contacta al administrador del sistema")
        sys.exit(1)


if __name__ == "__main__":
    main()
