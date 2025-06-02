import json
import hashlib
import os
from typing import Dict, Tuple, Optional


class AuthSystem:
    """
    Sistema de autenticación local que maneja registro, login y validación de usuarios.
    """

    def __init__(self, users_file: str = "users.json"):
        """
        Inicializa el sistema de autenticación.

        Args:
            users_file (str): Ruta del archivo JSON donde se guardan los usuarios
        """
        self.users_file = users_file
        self.failed_attempts = {}  # Contador de intentos fallidos por usuario
        self.max_attempts = 3

    def _hash_password(self, password: str) -> str:
        """
        Cifra una contraseña usando SHA-256.

        Args:
            password (str): Contraseña en texto plano

        Returns:
            str: Contraseña cifrada en hexadecimal
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> Dict:
        """
        Carga los usuarios desde el archivo JSON.

        Returns:
            Dict: Diccionario con los usuarios y sus contraseñas cifradas
        """
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return {}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_users(self, users: Dict) -> bool:
        """
        Guarda los usuarios en el archivo JSON.

        Args:
            users (Dict): Diccionario con usuarios y contraseñas

        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(self.users_file, 'w', encoding='utf-8') as file:
                json.dump(users, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")
            return False

    def register_user(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Registra un nuevo usuario en el sistema.

        Args:
            username (str): Nombre de usuario
            password (str): Contraseña en texto plano

        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Validaciones básicas
        if not username or not password:
            return False, "El nombre de usuario y la contraseña no pueden estar vacíos"

        if len(username) < 3:
            return False, "El nombre de usuario debe tener al menos 3 caracteres"

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"

        # Cargar usuarios existentes
        users = self._load_users()

        # Verificar si el usuario ya existe
        if username in users:
            return False, "El usuario ya existe"

        # Cifrar contraseña y agregar usuario
        hashed_password = self._hash_password(password)
        users[username] = {
            "password": hashed_password,
            "created_at": self._get_current_timestamp()
        }

        # Guardar en archivo
        if self._save_users(users):
            return True, "Usuario registrado exitosamente"
        else:
            return False, "Error al guardar el usuario"

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Valida las credenciales de un usuario.

        Args:
            username (str): Nombre de usuario
            password (str): Contraseña en texto plano

        Returns:
            Tuple[bool, str]: (éxito, mensaje)
        """
        # Verificar si el usuario está bloqueado
        if self._is_user_blocked(username):
            return False, f"Usuario bloqueado. Has superado el máximo de {self.max_attempts} intentos"

        # Cargar usuarios
        users = self._load_users()

        # Verificar si el usuario existe
        if username not in users:
            self._increment_failed_attempts(username)
            return False, "Usuario no encontrado"

        # Verificar contraseña
        hashed_password = self._hash_password(password)
        if users[username]["password"] == hashed_password:
            # Login exitoso - resetear intentos fallidos
            self._reset_failed_attempts(username)
            return True, "Login exitoso"
        else:
            # Contraseña incorrecta
            self._increment_failed_attempts(username)
            remaining = self.max_attempts - \
                self.failed_attempts.get(username, 0)
            if remaining <= 0:
                return False, f"Usuario bloqueado. Has superado el máximo de {self.max_attempts} intentos"
            else:
                return False, f"Contraseña incorrecta. Te quedan {remaining} intentos"

    def _is_user_blocked(self, username: str) -> bool:
        """
        Verifica si un usuario está bloqueado por exceso de intentos.

        Args:
            username (str): Nombre de usuario

        Returns:
            bool: True si está bloqueado, False en caso contrario
        """
        return self.failed_attempts.get(username, 0) >= self.max_attempts

    def _increment_failed_attempts(self, username: str) -> None:
        """
        Incrementa el contador de intentos fallidos para un usuario.

        Args:
            username (str): Nombre de usuario
        """
        self.failed_attempts[username] = self.failed_attempts.get(
            username, 0) + 1

    def _reset_failed_attempts(self, username: str) -> None:
        """
        Resetea el contador de intentos fallidos para un usuario.

        Args:
            username (str): Nombre de usuario
        """
        if username in self.failed_attempts:
            del self.failed_attempts[username]

    def _get_current_timestamp(self) -> str:
        """
        Obtiene el timestamp actual.

        Returns:
            str: Timestamp en formato ISO
        """
        from datetime import datetime
        return datetime.now().isoformat()

    def get_user_count(self) -> int:
        """
        Obtiene el número total de usuarios registrados.

        Returns:
            int: Número de usuarios
        """
        users = self._load_users()
        return len(users)

    def user_exists(self, username: str) -> bool:
        """
        Verifica si un usuario existe en el sistema.

        Args:
            username (str): Nombre de usuario

        Returns:
            bool: True si existe, False en caso contrario
        """
        users = self._load_users()
        return username in users

    def unblock_user(self, username: str) -> bool:
        """
        Desbloquea un usuario (función administrativa).

        Args:
            username (str): Nombre de usuario

        Returns:
            bool: True si se desbloqueó, False si no estaba bloqueado
        """
        if username in self.failed_attempts:
            del self.failed_attempts[username]
            return True
        return False
