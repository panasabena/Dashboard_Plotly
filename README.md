# 📊 Dashboard de Telecomunicaciones - Análisis de Churn

Un dashboard interactivo y moderno para el análisis completo de datos de churn (abandono) de clientes en empresas de telecomunicaciones.

## 🚀 Características

### 📈 Visualizaciones Interactivas
- **Análisis de Churn**: Distribución porcentual con gráfico de dona
- **Análisis Geográfico**: Tasa de churn por estado (Top 15)
- **Análisis de Uso**: Minutos, llamadas y cargos por período del día
- **Impacto de Servicios**: Planes internacionales y buzón de voz
- **Matriz de Correlación**: Relaciones entre variables
- **Análisis Predictivo**: PCA para reducción de dimensionalidad

### 🎨 Diseño Moderno
- **Bootstrap 5**: Diseño responsive y profesional
- **Font Awesome**: Iconos modernos
- **Tema Inter**: Tipografía elegante
- **Colores Corporativos**: Paleta profesional

### 🔧 Funcionalidades Avanzadas
- **Selector de Datasets**: Cambio dinámico entre datasets
- **Callbacks Inteligentes**: Actualización automática de gráficos
- **Hover Interactivo**: Información detallada en cada punto
- **Filtros Dinámicos**: Análisis segmentado

## 📋 Datasets Incluidos

- **Dataset Pequeño**: 669 registros (20% de la muestra)
- **Dataset Grande**: 2,668 registros (80% de la muestra)

### Variables Analizadas
- **Demográficas**: Estado, antigüedad de cuenta, código de área
- **Servicios**: Plan internacional, buzón de voz, mensajes
- **Uso**: Minutos, llamadas y cargos por período (día, tarde, noche)
- **Internacional**: Minutos, llamadas y cargos internacionales
- **Servicio al Cliente**: Número de llamadas
- **Target**: Variable de churn (Sí/No)

## 🛠️ Instalación

### Requisitos
- Python 3.11+
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd charter-project
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación**
```bash
python app.py
```

5. **Abrir en navegador**
```
http://localhost:8050
```

## 🌐 Despliegue Web

### Opción 1: Heroku (Recomendado)

1. **Crear cuenta en Heroku**
2. **Instalar Heroku CLI**
3. **Desplegar**
```bash
heroku create tu-dashboard-telecom
git add .
git commit -m "Initial deployment"
git push heroku main
```

### Opción 2: Railway

1. **Conectar repositorio a Railway**
2. **Configurar variables de entorno**
3. **Desplegar automáticamente**

### Opción 3: Render

1. **Crear cuenta en Render**
2. **Conectar repositorio**
3. **Configurar como servicio web**

### Opción 4: VPS/Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8050

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]
```

## 📊 Análisis Incluidos

### 1. **Métricas Principales**
- Total de clientes
- Tasa de churn
- Antigüedad promedio
- Llamadas a servicio al cliente promedio

### 2. **Análisis de Churn**
- Distribución porcentual
- Análisis por estado geográfico
- Identificación de estados con mayor riesgo

### 3. **Análisis de Uso**
- Distribución de minutos por período
- Relación entre llamadas y minutos
- Análisis de cargos por período
- Patrones de uso diurno/nocturno

### 4. **Impacto de Servicios**
- Efecto de planes internacionales en churn
- Influencia del buzón de voz
- Distribución de llamadas a servicio al cliente
- Análisis de mensajes de voz

### 5. **Análisis Predictivo**
- Matriz de correlación completa
- Análisis de componentes principales (PCA)
- Identificación de patrones ocultos

## 🎯 Insights Clave

### Factores de Riesgo de Churn
1. **Planes Internacionales**: Mayor tasa de churn
2. **Llamadas a Servicio**: Correlación positiva con churn
3. **Uso Nocturno**: Patrones específicos
4. **Antigüedad**: Relación con retención

### Recomendaciones Estratégicas
1. **Retención**: Enfoque en clientes con planes internacionales
2. **Servicio**: Mejorar atención al cliente
3. **Productos**: Desarrollar ofertas nocturnas
4. **Geografía**: Campañas específicas por estado

## 🔧 Personalización

### Modificar Colores
```python
# En app.py, cambiar los colores en los gráficos
marker_colors=['#tu-color-1', '#tu-color-2']
```

### Agregar Nuevos Gráficos
```python
@callback(
    Output('nuevo-grafico', 'figure'),
    [Input('data-store', 'data')]
)
def nuevo_analisis(data):
    # Tu código aquí
    pass
```

### Cambiar Tema
```python
# Cambiar el tema de Bootstrap
dbc.themes.COSMO  # o cualquier otro tema
```

## 📱 Responsive Design

El dashboard se adapta automáticamente a:
- **Desktop**: Layout completo
- **Tablet**: Reorganización de columnas
- **Mobile**: Stack vertical

## 🔒 Seguridad

- **Validación de datos**: Sanitización de inputs
- **Error handling**: Manejo robusto de errores
- **Rate limiting**: Protección contra sobrecarga

## 📈 Próximas Mejoras

- [ ] **Machine Learning**: Modelos predictivos
- [ ] **Alertas**: Notificaciones automáticas
- [ ] **Export**: Descarga de reportes
- [ ] **APIs**: Integración con sistemas externos
- [ ] **Real-time**: Actualización en tiempo real

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- 📧 Email: tu-email@ejemplo.com
- 💬 Issues: GitHub Issues
- 📖 Documentación: Wiki del proyecto

---

**Desarrollado con ❤️ usando Dash y Plotly**
