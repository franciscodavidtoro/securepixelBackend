

## 🔧 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- virtualenv (opcional pero recomendado)

---

## ⚙️ Pasos para ejecutar el proyecto

### 1. Crear y activar un entorno virtual

**Linux/macOS:**
```bash
python3 -m venv .env
source .env/bin/activate
```

**Windows (CMD):**
```cmd
python -m venv .env
.env\Scripts\activate
```

---

### 2. Instalar dependencias

Si ya tienes el archivo `requirements.txt`, ejecuta:

```bash
pip install -r requirements.txt
```

Si aún no lo tienes y quieres generarlo desde el entorno actual:

```bash
pip freeze > requirements.txt
```

---

### 3. Migraciones

Aplica las migraciones para crear las tablas en la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 4. Crear un superusuario

Crea un usuario administrador para acceder al panel `/admin`:

```bash
python manage.py createsuperuser
```

---

### 5. Iniciar el servidor de desarrollo

Inicia el servidor local:

```bash
python manage.py runserver
```

Abre tu navegador en:
```
http://127.0.0.1:8000/
```

Y para acceder al panel de administración:
```
http://127.0.0.1:8000/admin/
```

---
