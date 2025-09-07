# 🚀 Guía de Despliegue - Dashboard de Telecomunicaciones

## 🌐 Opciones de Despliegue

### 1. **Heroku (Recomendado para principiantes)**

#### Requisitos Previos
- Cuenta en [Heroku](https://heroku.com)
- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) instalado
- Git configurado

#### Pasos de Despliegue
```bash
# 1. Iniciar sesión en Heroku
heroku login

# 2. Crear aplicación
heroku create tu-dashboard-telecom

# 3. Configurar buildpacks
heroku buildpacks:set heroku/python

# 4. Agregar archivos al repositorio
git add .
git commit -m "Initial deployment"

# 5. Desplegar
git push heroku main

# 6. Abrir aplicación
heroku open
```

### 2. **Railway (Alternativa moderna)**

#### Pasos de Despliegue
1. Ir a [Railway](https://railway.app)
2. Conectar repositorio de GitHub
3. Configurar variables de entorno (si es necesario)
4. Desplegar automáticamente

### 3. **Render (Gratuito)**

#### Pasos de Despliegue
1. Ir a [Render](https://render.com)
2. Crear nuevo "Web Service"
3. Conectar repositorio
4. Configurar:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:server`
   - **Port**: `8050`

### 4. **Docker (Para desarrolladores avanzados)**

#### Despliegue Local con Docker
```bash
# Construir imagen
docker build -t telecom-dashboard .

# Ejecutar contenedor
docker run -p 8050:8050 telecom-dashboard
```

#### Despliegue con Docker Compose
```bash
# Ejecutar con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### 5. **VPS/Cloud Server**

#### Configuración en Ubuntu/Debian
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y dependencias
sudo apt install python3 python3-pip python3-venv nginx -y

# Clonar repositorio
git clone <tu-repositorio>
cd charter-project

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar Gunicorn como servicio
sudo nano /etc/systemd/system/telecom-dashboard.service
```

#### Archivo de servicio systemd
```ini
[Unit]
Description=Telecom Dashboard
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/charter-project
Environment="PATH=/home/ubuntu/charter-project/venv/bin"
ExecStart=/home/ubuntu/charter-project/venv/bin/gunicorn --workers 3 --bind unix:telecom-dashboard.sock -m 007 app:server

[Install]
WantedBy=multi-user.target
```

#### Configurar Nginx
```bash
sudo nano /etc/nginx/sites-available/telecom-dashboard
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/charter-project/telecom-dashboard.sock;
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/telecom-dashboard /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Iniciar servicio
sudo systemctl start telecom-dashboard
sudo systemctl enable telecom-dashboard
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Para producción
export FLASK_ENV=production
export DASH_DEBUG=False
export PORT=8050
```

### Optimización de Rendimiento
```python
# En app.py, agregar configuración de caché
from dash import Dash
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    # Configuración de caché
    cache_timeout=300,  # 5 minutos
    cache_default_timeout=300
)
```

### Monitoreo y Logs
```python
# Agregar logging
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# En callbacks
@callback(...)
def update_metrics(data):
    logger.info("Actualizando métricas")
    # ... código ...
```

## 🔒 Seguridad

### Configuración de Seguridad
```python
# Agregar middleware de seguridad
from flask_talisman import Talisman

Talisman(app.server, content_security_policy={
    'default-src': "'self'",
    'script-src': ["'self'", "'unsafe-inline'", "https://cdn.plot.ly"],
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
    'font-src': ["'self'", "https://fonts.gstatic.com"],
    'img-src': ["'self'", "data:", "https:"],
})
```

### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app.server,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

## 📊 Monitoreo

### Health Check
```python
@app.server.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

### Métricas de Rendimiento
```python
# Agregar métricas con prometheus
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app.server)
```

## 🚀 Despliegue Automático

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

## 📞 Soporte

### Troubleshooting Común

1. **Error de puerto ocupado**
   ```bash
   # Cambiar puerto
   export PORT=8051
   python app.py
   ```

2. **Error de dependencias**
   ```bash
   # Reinstalar dependencias
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

3. **Error de memoria**
   ```bash
   # Reducir workers de Gunicorn
   gunicorn --workers 1 --bind 0.0.0.0:8050 app:server
   ```

### Contacto
- 📧 Email: soporte@ejemplo.com
- 💬 Discord: [Canal de soporte]
- 📖 Wiki: [Documentación completa]

---

**¡Tu dashboard estará listo para producción! 🎉**
