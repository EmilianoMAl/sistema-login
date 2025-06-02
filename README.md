# 🔐 Sistema de Login Local en Python

## 📌 Descripción

Este proyecto implementa un sistema de autenticación local en Python que permite registrar usuarios, iniciar sesión y manejar contraseñas cifradas con SHA-256. Todo se guarda en un archivo JSON local, con validaciones, bloqueo por intentos fallidos y una interfaz de consola interactiva.

> 🔒 Diseñado como ejemplo educativo de buenas prácticas en seguridad, estructura modular y pruebas.

---

## ✨ Características principales

- Cifrado de contraseñas con SHA-256
- Control de intentos fallidos y bloqueo automático
- Registro y login con validación robusta
- Almacenamiento local en `users.json`
- Menús en consola con emojis y mensajes amigables
- Pruebas automatizadas (unitarias y de integración)
- Configuración avanzada separada en `config.py`

---

## 📁 Estructura del proyecto

```
sistema-login/
├── main.py               # Interfaz principal de usuario
├── auth_system.py        # Lógica de autenticación
├── config.py             # Configuración del sistema
├── test_sistema.py       # Archivo con pruebas automatizadas
├── README.md             # Documentación
└── users.json            # Archivo generado con los usuarios registrados
```

---

## ▶️ Cómo ejecutar

### Requisitos:
- Python 3.6 o superior
- No requiere librerías externas

### Ejecución:
```bash
python main.py
```

---

## 📋 Menús del sistema

### 🔹 Menú principal
- `1` – Registrar nuevo usuario
- `2` – Iniciar sesión
- `3` – Ver estadísticas
- `4` – Salir

### 🔹 Menú de usuario autenticado
- `1` – Ver información de la cuenta
- `2` – Cambiar usuario
- `3` – Ver estadísticas
- `4` – Cerrar sesión

---

## 🧪 Pruebas automatizadas

Puedes ejecutar las pruebas con:

```bash
python test_sistema.py
```

Incluyen validaciones para:
- Hash y seguridad
- Registro y login
- Intentos fallidos
- Operaciones con archivos
- Existencia de usuarios
- Integridad de datos en `users.json`

---

## 🔧 Seguridad y validaciones

- Contraseñas nunca se guardan en texto plano
- JSON estructurado con timestamp de creación
- Máximo 3 intentos antes de bloqueo
- Validación de longitud mínima en usuario y contraseña
- Entrada de contraseña oculta (`getpass`)
- Soporte para configuración extensible (`config.py`)

---

## 💡 Sugerencias de mejora

- Agregar recuperación de contraseña
- Añadir roles de usuario (admin, usuario)
- Guardar historial de logins
- Usar bcrypt o scrypt en vez de SHA-256
- Migrar a base de datos SQLite o PostgreSQL
- Crear una API o interfaz gráfica

---

## 📝 Licencia

Código abierto para uso educativo y personal.

---

## ✍️ Autor

**Emiliano Martínez**  
[GitHub](https://github.com/EmilianoMAl)  
[LinkedIn](https://www.linkedin.com/in/emiliano-martinez-40a6882b7/)

---

_Gracias por usar este sistema. ¡Tus datos están seguros!_
