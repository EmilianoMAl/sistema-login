# 🔐 Sistema de Login Local

Sistema de autenticación local desarrollado en Python que proporciona funcionalidades completas de registro y login con alta seguridad.

## 📋 Características

### 🔒 Seguridad

- **Cifrado de contraseñas** con SHA-256
- **Control de intentos fallidos** (máximo 3 intentos)
- **Bloqueo automático** después de exceder intentos
- **Validación de datos** de entrada

### 👤 Gestión de Usuarios

- **Registro** de nuevos usuarios
- **Login** con validación de credenciales
- **Información de cuenta** con fecha de registro
- **Cambio de usuario** sin reiniciar

### 💾 Almacenamiento

- **Persistencia** en archivo JSON local
- **Estructura organizada** de datos
- **Manejo de errores** en E/O de archivos

### 🖥️ Interfaz

- **Consola intuitiva** con menús claros
- **Emojis** para mejor experiencia visual
- **Mensajes informativos** y de error
- **Navegación fluida** entre opciones

## 🚀 Instalación y Uso

### Requisitos

- Python 3.6 o superior
- Módulos incluidos en Python estándar:
  - `json`
  - `hashlib`
  - `os`
  - `getpass`
  - `typing`

### Ejecución

```bash
python main.py
```

### Navegación

1. **Menú Principal:**

   - `1` - Registrar nuevo usuario
   - `2` - Iniciar sesión
   - `3` - Mostrar estadísticas
   - `4` - Salir

2. **Menú de Usuario Autenticado:**
   - `1` - Ver información de cuenta
   - `2` - Cambiar usuario
   - `3` - Ver estadísticas del sistema
   - `4` - Cerrar sesión

## 📁 Estructura del Proyecto

```
Sistema de Login/
│
├── main.py              # 🎯 Archivo principal con interfaz
├── auth_system.py       # 🔧 Sistema de autenticación
├── users.json          # 📊 Base de datos de usuarios (se crea automáticamente)
└── README.md           # 📖 Documentación
```

## 🔧 Componentes Técnicos

### `AuthSystem` (auth_system.py)

Clase principal que maneja toda la lógica de autenticación:

- `register_user()` - Registro de nuevos usuarios
- `login()` - Validación de credenciales
- `_hash_password()` - Cifrado SHA-256
- `_load_users()` / `_save_users()` - Manejo de archivo JSON
- `_is_user_blocked()` - Control de intentos fallidos
- `user_exists()` - Verificación de existencia
- `get_user_count()` - Estadísticas

### `LoginInterface` (main.py)

Interfaz de usuario con métodos para:

- `show_main_menu()` - Menú principal
- `register_user()` - Proceso de registro
- `login_user()` - Proceso de login
- `user_session()` - Sesión autenticada
- `show_stats()` - Estadísticas del sistema
- `clear_screen()` - Limpieza de pantalla

## 🛡️ Validaciones Implementadas

### Registro de Usuario

- ✅ Nombre de usuario mínimo 3 caracteres
- ✅ Contraseña mínima 6 caracteres
- ✅ Confirmación de contraseña
- ✅ Usuario único (no duplicados)
- ✅ Campos no vacíos

### Inicio de Sesión

- ✅ Verificación de existencia de usuario
- ✅ Validación de contraseña cifrada
- ✅ Control de intentos fallidos
- ✅ Bloqueo automático tras 3 intentos
- ✅ Campos no vacíos

## 📊 Formato del Archivo `users.json`

```json
{
  "usuario1": {
    "password": "hash_sha256_de_la_contraseña",
    "created_at": "2024-01-15T10:30:45.123456"
  },
  "usuario2": {
    "password": "otro_hash_sha256",
    "created_at": "2024-01-16T14:22:10.987654"
  }
}
```

## 🔄 Funcionalidades Extendibles

El sistema está diseñado para ser fácilmente extensible:

### 🌟 Mejoras Sugeridas

- **Recuperación de contraseña** mediante email
- **Roles de usuario** (admin, user, guest)
- **Historial de login** con timestamps
- **Configuración personalizable** (intentos máximos, longitud de contraseña)
- **Cifrado más avanzado** (bcrypt, scrypt)
- **Base de datos SQL** en lugar de JSON
- **Interfaz gráfica** con tkinter o PyQt
- **API REST** para integración web

### 🔧 Puntos de Extensión

1. **Clase `AuthSystem`**: Agregar nuevos métodos de validación
2. **Archivo de configuración**: Para parámetros del sistema
3. **Clase `User`**: Para representar usuarios con más atributos
4. **Logging**: Para auditoría y debugging
5. **Encriptación**: Para proteger el archivo JSON

## 🐛 Manejo de Errores

- ✅ **Archivos corruptos**: Recreación automática del JSON
- ✅ **Permisos de escritura**: Mensaje de error informativo
- ✅ **Interrupciones**: Ctrl+C manejado elegantemente
- ✅ **Entradas inválidas**: Validación y mensaje de ayuda
- ✅ **Errores inesperados**: Captura y logging

## 🔒 Consideraciones de Seguridad

### ✅ Implementado

- Contraseñas nunca almacenadas en texto plano
- Hash SHA-256 para cifrado
- Entrada de contraseña oculta (`getpass`)
- Control de intentos de fuerza bruta
- Validación de entrada de usuario

### ⚠️ Recomendaciones Adicionales

- Usar salt único para cada contraseña
- Implementar rate limiting temporal
- Logs de seguridad para auditoría
- Backup automático del archivo de usuarios
- Cifrado del archivo JSON completo

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Sistema desarrollado como ejemplo de buenas prácticas en Python para sistemas de autenticación local.

---

_¡Disfruta usando el Sistema de Login Local! 🎉_
