# =============================================================================
# DASHBOARD DE TELECOMUNICACIONES - ANÁLISIS DE CHURN
# =============================================================================
# Este dashboard analiza datos de clientes de telecomunicaciones para identificar
# patrones de churn (abandono) y comportamiento de clientes.
# 
# ESTRUCTURA:
# 1. Imports y configuración
# 2. Layout principal (interfaz visual)
# 3. Callbacks (funciones que actualizan los gráficos)
# 4. Configuración del servidor
# =============================================================================

# =============================================================================
# 1. IMPORTS Y LIBRERÍAS NECESARIAS
# =============================================================================
import dash
from dash import dcc, html, Input, Output, callback, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
import time
warnings.filterwarnings('ignore')

# =============================================================================
# 2. CONFIGURACIÓN DE LA APLICACIÓN DASH
# =============================================================================
# Crear la aplicación Dash con Bootstrap y estilos personalizados
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,        # Tema de Bootstrap para diseño responsivo
        dbc.icons.FONT_AWESOME,      # Iconos de Font Awesome
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"  # Fuente personalizada
    ],
    suppress_callback_exceptions=True  # Evita errores cuando los callbacks no encuentran elementos
)

# Título que aparece en la pestaña del navegador
app.title = "Dashboard Billing Ops - Test Data"

# =============================================================================
# 3. LAYOUT PRINCIPAL - ESTRUCTURA VISUAL DEL DASHBOARD
# =============================================================================
# El layout define cómo se ve el dashboard en el navegador
# Usa componentes de Bootstrap para un diseño profesional y responsivo

# =====================================================================
# PANTALLA DE CARGA (LOADING SCREEN)
# =====================================================================
loading_screen = html.Div([
    # Imagen de fondo que ocupa toda la pantalla
    html.Img(
        src="/assets/Charter Lockup.png",  # Ruta a la imagen
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1'
        }
    ),
    # Overlay con texto de carga en la parte inferior
    html.Div([
        # Texto de carga con animación
        html.Div([
            html.H2("Loading", id="loading-text", className="text-white fw-bold", 
                   style={'fontSize': '2.5rem', 'textShadow': '2px 2px 4px rgba(0,0,0,0.5)', 'marginBottom': '10px'}),
            html.Div(id="loading-dots", className="text-white fw-bold",
                    style={'fontSize': '2.5rem', 'textShadow': '2px 2px 4px rgba(0,0,0,0.5)'})
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        # Spinner de Bootstrap
        html.Div([
            dbc.Spinner(color="white", size="lg")
        ], style={'textAlign': 'center'})
    ], style={
        'position': 'absolute',
        'bottom': '10%',
        'left': '50%',
        'transform': 'translateX(-50%)',
        'zIndex': '1'
    })
], style={
    'position': 'relative',
    'width': '100vw',
    'height': '100vh',
    'overflow': 'hidden'
})

# =====================================================================
# DASHBOARD PRINCIPAL
# =====================================================================
main_dashboard = dbc.Container([
    
    # =====================================================================
    # HEADER - TÍTULO Y NAVEGACIÓN
    # =====================================================================
    dbc.Row([
        # Columna izquierda: Título y descripción
        dbc.Col([
            html.H1([
                html.I(className="fas fa-chart-line me-3"),  # Icono de gráfico
                "Dashboard Billing Ops"
            ], className="text-primary fw-bold mb-0"),  # Clases de Bootstrap para estilos
            html.P("Complete Analysis of Churn and Customer Behavior", 
                   className="text-muted mb-4")
        ], width=6),  # Ocupa 6 columnas de 12 (1/2 del ancho)
        
        # Columna derecha: Dropdown para seleccionar dataset
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Select Dataset:", className="form-label fw-bold"),
                    dcc.Dropdown(
                        id='dataset-selector',  # ID único para referenciar este elemento
                        options=[
                            {'label': 'Dataset Pequeño (20% - 669 registros)', 'value': 'churn-20'},
                            {'label': 'Dataset Grande (80% - 2,668 registros)', 'value': 'churn-80'}
                        ],
                        value='churn-80',  # Valor por defecto
                        className="mb-0"
                    )
                ])
            ], className="border-0 shadow-sm")  # Sin borde, con sombra sutil
        ], width=6)  # Ocupa 6 columnas de 12 (1/2 del ancho)
    ], className="mb-4"),  # Margen inferior
    
    # =====================================================================
    # NAVEGACIÓN CON PESTAÑAS
    # =====================================================================
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Dashboard", tab_id="dashboard-tab", id="dashboard-tab"),
                dbc.Tab(label="Guide", tab_id="guide-tab", id="guide-tab")
            ], id="tabs", active_tab="dashboard-tab"),
            html.Div(id="tab-content")
        ], width=12)
    ], className="mb-4"),
    
], fluid=True, className="py-4")  # Container fluido con padding vertical

# =====================================================================
# CONTENIDO DEL DASHBOARD (PARA LA PESTAÑA)
# =====================================================================
dashboard_content = html.Div([
    # Imagen de fondo que ocupa toda la pantalla
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",  # Ruta a la imagen de fondo
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'  # Hacer la imagen sutilmente transparente para no interferir con el contenido
        }
    ),
    # Contenido del dashboard con fondo semi-transparente
    dbc.Container([
        # Store para datos
        dcc.Store(id='data-store', data=[]),
        
        # Selector de dataset (solo visible en la pestaña Dashboard)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Label("Select Dataset:", className="form-label fw-bold"),
                        dcc.Dropdown(
                            id='dataset-selector',  # ID único para referenciar este elemento
                            options=[
                                {'label': 'Dataset Pequeño (20% - 669 registros)', 'value': 'churn-20'},
                                {'label': 'Dataset Grande (80% - 2,668 registros)', 'value': 'churn-80'}
                            ],
                            value='churn-80',  # Valor por defecto
                            className="mb-0"
                        )
                    ])
                ], className="border-0 shadow-sm")  # Sin borde, con sombra sutil
            ], width=12)
        ], className="mb-4"),
    
    # Métricas principales
    dbc.Row([
        # Tarjeta 1: Total de Clientes
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='total-customers', className="text-primary fw-bold"),  # ID para actualizar el valor
                    html.P("Total Customers", className="text-muted mb-0")
                ])
            ], className="border-0 shadow-sm text-center")
        ], width=3),  # Cada tarjeta ocupa 3 columnas (4 tarjetas = 12 columnas)
        
        # Tarjeta 2: Tasa de Churn
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='churn-rate', className="text-danger fw-bold"),  # Rojo para indicar problema
                    html.P("Churn Rate", className="text-muted mb-0")
                ])
            ], className="border-0 shadow-sm text-center")
        ], width=3),
        
        # Tarjeta 3: Antigüedad Promedio
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='avg-account-length', className="text-success fw-bold"),  # Verde para métrica positiva
                    html.P("Average Account Length", className="text-muted mb-0")
                ])
            ], className="border-0 shadow-sm text-center")
        ], width=3),
        
        # Tarjeta 4: Llamadas a Servicio al Cliente
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='avg-customer-service', className="text-warning fw-bold"),  # Amarillo para advertencia
                    html.P("Average Customer Service Calls", className="text-muted mb-0")
                ])
            ], className="border-0 shadow-sm text-center")
        ], width=3)
    ], className="mb-4"),
    
    # Gráficos principales
    dbc.Row([
        # Gráfico 1: Análisis de Churn (Gráfico de dona)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-exclamation-triangle me-2"),  # Icono de advertencia
                        "Churn Distribution"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='churn-distribution')  # Componente de gráfico de Plotly
                ])
            ], className="border-0 shadow-sm")
        ], width=6),  # Ocupa la mitad del ancho
        
        # Gráfico 2: Churn por Estado (Gráfico de barras horizontales)
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-map-marker-alt me-2"),  # Icono de ubicación
                        "Churn Rate by State"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='churn-by-state')
                ])
            ], className="border-0 shadow-sm")
        ], width=6)  # Ocupa la otra mitad del ancho
    ], className="mb-4"),
    
    # Análisis de uso
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-phone me-2"),  # Icono de teléfono
                        "Periodic Usage Analysis"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='usage-analysis')  # Contendrá 4 subplots
                ])
            ], className="border-0 shadow-sm")
        ], width=12)  # Ocupa todo el ancho
    ], className="mb-4"),
    
    # Análisis de servicios y correlaciones
    dbc.Row([
        # Gráfico 1: Impacto de Servicios en Churn
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-cogs me-2"),  # Icono de engranajes
                        "Services Impact on Churn"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='services-impact')  # Contendrá 4 subplots
                ])
            ], className="border-0 shadow-sm")
        ], width=6),
        
        # Gráfico 2: Matriz de Correlación
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-bar me-2"),  # Icono de gráfico de barras
                        "Correlation Matrix"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='correlation-matrix')  # Heatmap de correlaciones
                ])
            ], className="border-0 shadow-sm")
        ], width=6)
    ], className="mb-4"),
    
    # Análisis predictivo
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-brain me-2"),  # Icono de cerebro (IA)
                        "Predictive Analysis - PCA"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='pca-analysis')  # Visualización 2D de clientes
                ])
            ], className="border-0 shadow-sm")
        ], width=12)  # Ocupa todo el ancho
    ], className="mb-4")
    
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# =====================================================================
# PÁGINA DE ÍNDICE - EXPLICACIONES DE GRÁFICOS
# =====================================================================
index_page = html.Div([
    # Imagen de fondo que ocupa toda la pantalla
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",  # Ruta a la imagen de fondo
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'  # Hacer la imagen sutilmente transparente para no interferir con el contenido
        }
    ),
    # Contenido de la guía con fondo semi-transparente
    dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1([
                    html.I(className="fas fa-book me-3"),
                    "Dashboard Guide - Understanding the Charts"
                ], className="text-primary fw-bold mb-0"),
                html.P("Complete explanation of each chart and metric in the dashboard", 
                       className="text-muted mb-4")
            ], width=12)
        ], className="mb-4"),
    
    # Métricas Principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-pie me-2"),
                        "Key Metrics"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.H6("Total Customers", className="text-primary fw-bold"),
                    html.P("The total number of customers in the selected dataset. This metric shows the sample size being analyzed.", className="text-muted"),
                    
                    html.H6("Churn Rate", className="text-danger fw-bold mt-3"),
                    html.P("Percentage of customers who have left the service. A higher churn rate indicates customer dissatisfaction or competitive pressure.", className="text-muted"),
                    
                    html.H6("Average Account Length", className="text-success fw-bold mt-3"),
                    html.P("Average number of days customers have been with the service. Longer account lengths typically indicate higher customer loyalty.", className="text-muted"),
                    
                    html.H6("Average Customer Service Calls", className="text-warning fw-bold mt-3"),
                    html.P("Average number of calls made to customer service. Higher numbers may indicate service issues or customer dissatisfaction.", className="text-muted")
                ])
            ], className="border-0 shadow-sm")
        ], width=12)
    ], className="mb-4"),
    
    # Gráficos Principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "Churn Distribution"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P("This donut chart shows the proportion of customers who have churned (left the service) versus those who remain active.", className="text-muted"),
                    html.Ul([
                        html.Li("Red section: Customers who have churned"),
                        html.Li("Green section: Active customers"),
                        html.Li("The size of each section represents the percentage of customers in each category")
                    ], className="text-muted")
                ])
            ], className="border-0 shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-map-marker-alt me-2"),
                        "Churn Rate by State"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P("This horizontal bar chart displays the top 15 states with the highest churn rates.", className="text-muted"),
                    html.Ul([
                        html.Li("Each bar represents a different state"),
                        html.Li("Bar length shows the percentage of customers who churned in that state"),
                        html.Li("Helps identify geographic patterns in customer retention"),
                        html.Li("Useful for targeted retention strategies by region")
                    ], className="text-muted")
                ])
            ], className="border-0 shadow-sm")
        ], width=6)
    ], className="mb-4"),
    
    # Análisis de Uso
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-phone me-2"),
                        "Periodic Usage Analysis"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P("This comprehensive analysis shows usage patterns across different time periods of the day.", className="text-muted"),
                    html.H6("Four Subplots:", className="fw-bold mt-3"),
                    html.Ul([
                        html.Li("Minutes by Period: Box plots showing call duration distribution for day, evening, and night"),
                        html.Li("Calls by Period: Box plots showing number of calls distribution for each period"),
                        html.Li("Charges by Period: Box plots showing billing amounts for each time period"),
                        html.Li("Minutes vs Calls: Scatter plot showing relationship between call frequency and duration")
                    ], className="text-muted"),
                    html.P("This analysis helps understand usage patterns and can inform pricing strategies and network capacity planning.", className="text-muted mt-3")
                ])
            ], className="border-0 shadow-sm")
        ], width=12)
    ], className="mb-4"),
    
    # Servicios y Correlaciones
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-cogs me-2"),
                        "Services Impact on Churn"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P("This analysis examines how different service features affect customer churn rates.", className="text-muted"),
                    html.H6("Four Subplots:", className="fw-bold mt-3"),
                    html.Ul([
                        html.Li("International Plan vs Churn: Bar chart showing churn rates for customers with/without international calling"),
                        html.Li("Voice Mail Plan vs Churn: Bar chart showing churn rates for customers with/without voicemail"),
                        html.Li("Customer Service Calls: Histogram showing distribution of customer service call frequency"),
                        html.Li("Voice Mail Messages: Histogram showing distribution of voicemail usage")
                    ], className="text-muted"),
                    html.P("This helps identify which services contribute to customer retention or dissatisfaction.", className="text-muted mt-3")
                ])
            ], className="border-0 shadow-sm")
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-chart-bar me-2"),
                        "Correlation Matrix"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P("This heatmap shows the correlation between all numerical variables in the dataset.", className="text-muted"),
                    html.Ul([
                        html.Li("Red colors indicate positive correlations"),
                        html.Li("Blue colors indicate negative correlations"),
                        html.Li("Darker colors indicate stronger correlations"),
                        html.Li("White/light colors indicate weak or no correlation")
                    ], className="text-muted"),
                    html.P("This helps identify which factors are most strongly related to churn and customer behavior.", className="text-muted mt-3")
                ])
            ], className="border-0 shadow-sm")
        ], width=6)
    ], className="mb-4"),
    
    # Análisis Predictivo
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5([
                        html.I(className="fas fa-brain me-2"),
                        "Predictive Analysis - PCA"
                    ], className="mb-0")
                ]),
                dbc.CardBody([
                    html.P("Principal Component Analysis (PCA) reduces the complexity of customer data to visualize patterns in 2D.", className="text-muted"),
                    html.Ul([
                        html.Li("Green dots: Customers who have not churned"),
                        html.Li("Red dots: Customers who have churned"),
                        html.Li("Each dot represents a customer positioned based on their usage patterns"),
                        html.Li("Clusters of similar colors may indicate customer segments")
                    ], className="text-muted"),
                    html.P("This visualization helps identify customer segments and predict which customers are at risk of churning based on their usage patterns.", className="text-muted mt-3")
                ])
            ], className="border-0 shadow-sm")
        ], width=12)
    ], className="mb-4")
    
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# =====================================================================
# LAYOUT PRINCIPAL CON SISTEMA DE CARGA Y NAVEGACIÓN
# =====================================================================
app.layout = html.Div([
    # Store para controlar la visibilidad
    dcc.Store(id='loading-state', data={'show_loading': True}),
    
    # Intervalo para la animación de puntos suspensivos
    dcc.Interval(
        id='loading-interval',
        interval=500,  # Actualizar cada 500ms
        n_intervals=0,
        disabled=False
    ),
    
    # Intervalo para cambiar de pantalla de carga al dashboard
    dcc.Interval(
        id='dashboard-interval',
        interval=2000,  # 2 segundos
        n_intervals=0,
        disabled=False
    ),
    
    # Contenedor principal que cambia entre loading y dashboard
    html.Div(id='main-content')
])

# =============================================================================
# 4. CALLBACKS - FUNCIONES QUE ACTUALIZAN LOS GRÁFICOS
# =============================================================================
# Los callbacks son funciones que se ejecutan automáticamente cuando cambian
# los inputs (como el selector de dataset) y actualizan los outputs (como los gráficos)

# =====================================================================
# CALLBACK 1: ANIMACIÓN DE PUNTOS SUSPENSIVOS
# =====================================================================
@callback(
    Output('loading-dots', 'children'),
    Input('loading-interval', 'n_intervals')
)
def update_loading_dots(n):
    """
    Crea la animación de puntos suspensivos en el texto "Loading".
    
    Args:
        n (int): Número de intervalos transcurridos
    
    Returns:
        str: Puntos suspensivos animados
    """
    dots = "." * ((n % 4) + 1)  # 1 a 4 puntos
    return dots

# =====================================================================
# CALLBACK 2: CAMBIO DE PANTALLA DE CARGA AL DASHBOARD
# =====================================================================
@callback(
    Output('main-content', 'children'),
    Output('loading-interval', 'disabled'),
    Output('dashboard-interval', 'disabled'),
    Input('dashboard-interval', 'n_intervals'),
    Input('loading-state', 'data')
)
def switch_to_dashboard(n_intervals, loading_data):
    """
    Cambia de la pantalla de carga al dashboard principal después de 2 segundos.
    
    Args:
        n_intervals (int): Número de intervalos transcurridos
        loading_data (dict): Estado de carga
    
    Returns:
        tuple: Contenido principal, estado de intervalos
    """
    if n_intervals >= 2:  # Después de 2 segundos (1 intervalo de 2000ms)
        return main_dashboard, True, True  # Mostrar dashboard, deshabilitar intervalos
    else:
        return loading_screen, False, False  # Mostrar loading, mantener intervalos activos

# =====================================================================
# CALLBACK 3: NAVEGACIÓN ENTRE PESTAÑAS
# =====================================================================
@callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
)
def switch_tab(active_tab):
    """
    Cambia entre las pestañas del dashboard (Dashboard y Guide).
    
    Args:
        active_tab (str): ID de la pestaña activa
    
    Returns:
        html.Div: Contenido de la pestaña seleccionada
    """
    if active_tab == "dashboard-tab":
        return dashboard_content
    elif active_tab == "guide-tab":
        return index_page
    else:
        return dashboard_content  # Por defecto, mostrar dashboard

# =====================================================================
# CALLBACK 4: CARGA DE DATOS INICIALES
# =====================================================================
# Este callback se ejecuta cuando se selecciona un dataset diferente
@callback(
    Output('data-store', 'data'),           # Output: almacena los datos en el store
    Input('dataset-selector', 'value'),     # Input: valor seleccionado en el dropdown
    prevent_initial_call=False              # Se ejecuta también al cargar la página
)
def load_initial_data(dataset):
    """
    Carga los datos del CSV seleccionado y los prepara para el análisis.
    
    Args:
        dataset (str): 'churn-20' o 'churn-80'
    
    Returns:
        list: Lista de diccionarios con los datos del CSV
    """
    try:
        # Cargar el archivo CSV según la selección
        if dataset == 'churn-20':
            df = pd.read_csv('Data/churn-bigml-20.csv')
        else:
            df = pd.read_csv('Data/churn-bigml-80.csv')
        
        # Convertir columnas booleanas de 'Yes'/'No' a True/False
        df['International plan'] = df['International plan'].map({'Yes': True, 'No': False})
        df['Voice mail plan'] = df['Voice mail plan'].map({'Yes': True, 'No': False})
        df['Churn'] = df['Churn'].map({True: 'Yes', False: 'No'})  # Convertir a español
        
        print(f"✅ Datos cargados: {len(df)} registros")
        return df.to_dict('records')  # Convertir DataFrame a lista de diccionarios
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return []

# =====================================================================
# CALLBACK 5: ACTUALIZACIÓN DE MÉTRICAS PRINCIPALES
# =====================================================================
# Este callback actualiza las 4 tarjetas de métricas cuando cambian los datos
@callback(
    [Output('total-customers', 'children'),           # Total de clientes
     Output('churn-rate', 'children'),                # Tasa de churn
     Output('avg-account-length', 'children'),        # Antigüedad promedio
     Output('avg-customer-service', 'children')],     # Llamadas promedio
    [Input('data-store', 'data')]                     # Input: datos del store
)
def update_metrics(data):
    """
    Calcula y actualiza las métricas principales del dashboard.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        tuple: 4 valores con las métricas calculadas
    """
    if not data:  # Si no hay datos, retornar valores por defecto
        return "0", "0%", "0", "0"
    
    df = pd.DataFrame(data)  # Convertir lista a DataFrame
    
    # Calcular métricas
    total_customers = len(df)  # Número total de clientes
    churn_rate = f"{(df['Churn'] == 'Yes').mean() * 100:.1f}%"  # Porcentaje de churn
    avg_account_length = f"{df['Account length'].mean():.0f} days"  # Antigüedad promedio
    avg_customer_service = f"{df['Customer service calls'].mean():.1f}"  # Llamadas promedio
    
    return total_customers, churn_rate, avg_account_length, avg_customer_service

# =====================================================================
# CALLBACK 6: DISTRIBUCIÓN DE CHURN (GRÁFICO DE DONA)
# =====================================================================
# Este callback crea un gráfico de dona que muestra la proporción de churn
@callback(
    Output('churn-distribution', 'figure'),  # Output: gráfico de dona
    [Input('data-store', 'data')]            # Input: datos del store
)
def update_churn_distribution(data):
    """
    Crea un gráfico de dona que muestra la distribución de churn.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        go.Figure: Gráfico de dona de Plotly
    """
    if not data:
        return go.Figure()  # Gráfico vacío si no hay datos
    
    df = pd.DataFrame(data)
    churn_counts = df['Churn'].value_counts()  # Contar Sí/No churn
    
    # Crear gráfico de dona (pie chart con agujero)
    fig = go.Figure(data=[go.Pie(
        labels=churn_counts.index,           # Etiquetas: 'Yes', 'No'
        values=churn_counts.values,          # Valores: cantidad de cada uno
        hole=0.6,                           # Tamaño del agujero (0.6 = 60%)
        marker_colors=['#dc3545', '#28a745'],  # Rojo para churn, verde para no churn
        textinfo='label+percent',            # Mostrar etiqueta y porcentaje
        textfont_size=14
    )])
    
    # Configurar el layout del gráfico
    fig.update_layout(
        title="Churn Distribution",
        showlegend=True,
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)  # Márgenes
    )
    
    return fig

# =====================================================================
# CALLBACK 7: CHURN POR ESTADO (GRÁFICO DE BARRAS HORIZONTALES)
# =====================================================================
# Este callback crea un gráfico de barras horizontales con los estados con mayor churn
@callback(
    Output('churn-by-state', 'figure'),     # Output: gráfico de barras
    [Input('data-store', 'data')]           # Input: datos del store
)
def update_churn_by_state(data):
    """
    Crea un gráfico de barras horizontales con la tasa de churn por estado.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        go.Figure: Gráfico de barras horizontales de Plotly
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Calcular tasa de churn por estado y ordenar de mayor a menor
    state_churn = df.groupby('State')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100  # Porcentaje de churn por estado
    ).sort_values(ascending=False).head(15)  # Top 15 estados
    
    # Crear gráfico de barras horizontales
    fig = go.Figure(data=[go.Bar(
        x=state_churn.values,                    # Valores en el eje X (porcentajes)
        y=state_churn.index,                     # Estados en el eje Y
        orientation='h',                         # Barras horizontales
        marker_color='#dc3545',                  # Color rojo
        text=[f'{val:.1f}%' for val in state_churn.values],  # Texto con porcentaje
        textposition='auto'                      # Posición automática del texto
    )])
    
    # Configurar el layout
    fig.update_layout(
        title="Churn Rate by State (Top 15)",
        xaxis_title="Churn Rate (%)",
        yaxis_title="State",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# =====================================================================
# CALLBACK 8: ANÁLISIS DE USO POR PERÍODO (4 SUBPLOTS)
# =====================================================================
# Este callback crea 4 gráficos que analizan el uso de servicios por período
@callback(
    Output('usage-analysis', 'figure'),     # Output: gráfico con 4 subplots
    [Input('data-store', 'data')]           # Input: datos del store
)
def update_usage_analysis(data):
    """
    Crea 4 subplots que analizan el uso de servicios por período del día.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        go.Figure: Gráfico con 4 subplots de Plotly
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Crear subplots: 2 filas x 2 columnas
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Minutes by Period', 'Calls by Period', 
                       'Charges by Period', 'Minutes vs Calls'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Definir períodos y colores
    periods = ['Total day minutes', 'Total eve minutes', 'Total night minutes']
    colors = ['#007bff', '#28a745', '#ffc107']  # Azul, verde, amarillo
    
    # SUBPLOT 1: Minutos por período (Box plots)
    for i, period in enumerate(periods):
        fig.add_trace(
            go.Box(y=df[period], 
                   name=period.replace('Total ', '').replace(' minutes', '').title(),
                   marker_color=colors[i]),
            row=1, col=1
        )
    
    # SUBPLOT 2: Llamadas por período (Box plots)
    call_periods = ['Total day calls', 'Total eve calls', 'Total night calls']
    for i, period in enumerate(call_periods):
        fig.add_trace(
            go.Box(y=df[period], 
                   name=period.replace('Total ', '').replace(' calls', '').title(),
                   marker_color=colors[i]),
            row=1, col=2
        )
    
    # SUBPLOT 3: Cargos por período (Box plots)
    charge_periods = ['Total day charge', 'Total eve charge', 'Total night charge']
    for i, period in enumerate(charge_periods):
        fig.add_trace(
            go.Box(y=df[period], 
                   name=period.replace('Total ', '').replace(' charge', '').title(),
                   marker_color=colors[i]),
            row=2, col=1
        )
    
    # SUBPLOT 4: Relación minutos vs llamadas (Scatter plots)
    fig.add_trace(
        go.Scatter(x=df['Total day calls'], y=df['Total day minutes'],
                   mode='markers', name='Día',
                   marker=dict(color='#007bff', opacity=0.6)),
        row=2, col=2
    )
    
    fig.add_trace(
        go.Scatter(x=df['Total eve calls'], y=df['Total eve minutes'],
                   mode='markers', name='Noche',
                   marker=dict(color='#28a745', opacity=0.6)),
        row=2, col=2
    )
    
    # Configurar el layout
    fig.update_layout(
        height=600,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# =====================================================================
# CALLBACK 9: IMPACTO DE SERVICIOS EN CHURN (4 SUBPLOTS)
# =====================================================================
# Este callback analiza cómo los diferentes servicios afectan el churn
@callback(
    Output('services-impact', 'figure'),    # Output: gráfico con 4 subplots
    [Input('data-store', 'data')]           # Input: datos del store
)
def update_services_impact(data):
    """
    Crea 4 subplots que analizan el impacto de servicios en el churn.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        go.Figure: Gráfico con 4 subplots de Plotly
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Crear subplots: 2 filas x 2 columnas
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('International Plan vs Churn', 'Voice Mail Plan vs Churn',
                       'Customer Service Calls', 'Voice Mail Messages'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # SUBPLOT 1: Plan Internacional vs Churn
    intl_churn = df.groupby('International plan')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100  # Tasa de churn por plan internacional
    )
    
    fig.add_trace(
        go.Bar(x=intl_churn.index, y=intl_churn.values,
               marker_color=['#28a745', '#dc3545'],  # Verde para No, rojo para Sí
               text=[f'{val:.1f}%' for val in intl_churn.values],
               textposition='auto'),
        row=1, col=1
    )
    
    # SUBPLOT 2: Buzón de Voz vs Churn
    vmail_churn = df.groupby('Voice mail plan')['Churn'].apply(
        lambda x: (x == 'Yes').mean() * 100  # Tasa de churn por buzón de voz
    )
    
    fig.add_trace(
        go.Bar(x=vmail_churn.index, y=vmail_churn.values,
               marker_color=['#28a745', '#dc3545'],
               text=[f'{val:.1f}%' for val in vmail_churn.values],
               textposition='auto'),
        row=1, col=2
    )
    
    # SUBPLOT 3: Distribución de llamadas a servicio al cliente
    fig.add_trace(
        go.Histogram(x=df['Customer service calls'], nbinsx=10,
                     marker_color='#ffc107'),  # Amarillo
        row=2, col=1
    )
    
    # SUBPLOT 4: Distribución de mensajes de voz
    fig.add_trace(
        go.Histogram(x=df['Number vmail messages'], nbinsx=15,
                     marker_color='#17a2b8'),  # Azul claro
        row=2, col=2
    )
    
    # Configurar el layout
    fig.update_layout(
        height=500,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# =====================================================================
# CALLBACK 10: MATRIZ DE CORRELACIÓN (HEATMAP)
# =====================================================================
# Este callback crea un heatmap que muestra las correlaciones entre variables
@callback(
    Output('correlation-matrix', 'figure'),  # Output: heatmap de correlación
    [Input('data-store', 'data')]            # Input: datos del store
)
def update_correlation_matrix(data):
    """
    Crea un heatmap que muestra las correlaciones entre todas las variables numéricas.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        go.Figure: Heatmap de correlación de Plotly
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Seleccionar variables numéricas para el análisis de correlación
    numeric_cols = ['Account length', 'Number vmail messages', 'Total day minutes',
                   'Total day calls', 'Total day charge', 'Total eve minutes',
                   'Total eve calls', 'Total eve charge', 'Total night minutes',
                   'Total night calls', 'Total night charge', 'Total intl minutes',
                   'Total intl calls', 'Total intl charge', 'Customer service calls']
    
    # Convertir variables booleanas a numéricas para incluir en la correlación
    df['International plan'] = df['International plan'].astype(int)
    df['Voice mail plan'] = df['Voice mail plan'].astype(int)
    df['Churn'] = (df['Churn'] == 'Yes').astype(int)
    
    # Calcular matriz de correlación
    corr_matrix = df[numeric_cols + ['International plan', 'Voice mail plan', 'Churn']].corr()
    
    # Crear heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,                    # Valores de correlación
        x=corr_matrix.columns,                   # Variables en eje X
        y=corr_matrix.columns,                   # Variables en eje Y
        colorscale='RdBu',                       # Escala de colores: Rojo-Azul
        zmid=0,                                  # Valor medio (0 = sin correlación)
        text=np.round(corr_matrix.values, 2),    # Texto con valores redondeados
        texttemplate="%{text}",                  # Formato del texto
        textfont={"size": 8}                     # Tamaño de fuente
    ))
    
    # Configurar el layout
    fig.update_layout(
        title="Correlation Matrix",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# =====================================================================
# CALLBACK 11: ANÁLISIS PCA (COMPONENTES PRINCIPALES)
# =====================================================================
# Este callback realiza análisis de componentes principales para visualizar clientes en 2D
@callback(
    Output('pca-analysis', 'figure'),       # Output: gráfico de dispersión 2D
    [Input('data-store', 'data')]           # Input: datos del store
)
def update_pca_analysis(data):
    """
    Realiza análisis de componentes principales (PCA) para visualizar clientes en 2D.
    
    Args:
        data (list): Lista de diccionarios con los datos de clientes
    
    Returns:
        go.Figure: Gráfico de dispersión 2D con clientes coloreados por churn
    """
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    
    # Preparar datos para PCA: seleccionar características numéricas
    features = ['Account length', 'Number vmail messages', 'Total day minutes',
               'Total day calls', 'Total day charge', 'Total eve minutes',
               'Total eve calls', 'Total eve charge', 'Total night minutes',
               'Total night calls', 'Total night charge', 'Total intl minutes',
               'Total intl calls', 'Total intl charge', 'Customer service calls']
    
    # Convertir variables booleanas a numéricas
    df['International plan'] = df['International plan'].astype(int)
    df['Voice mail plan'] = df['Voice mail plan'].astype(int)
    df['Churn'] = (df['Churn'] == 'Yes').astype(int)
    
    # Agregar variables booleanas a las características
    features.extend(['International plan', 'Voice mail plan', 'Churn'])
    
    # Aplicar PCA: normalizar datos y reducir a 2 dimensiones
    scaler = StandardScaler()  # Normalizar datos (media=0, desv=1)
    scaled_data = scaler.fit_transform(df[features])
    
    pca = PCA(n_components=2)  # Reducir a 2 componentes principales
    pca_result = pca.fit_transform(scaled_data)
    
    # Crear figura
    fig = go.Figure()
    
    # Colorear puntos por churn: verde para no churn (0), rojo para churn (1)
    colors = ['#28a745' if x == 0 else '#dc3545' for x in df['Churn']]
    
    # Agregar scatter plot
    fig.add_trace(go.Scatter(
        x=pca_result[:, 0],                    # Componente principal 1
        y=pca_result[:, 1],                    # Componente principal 2
        mode='markers',                        # Modo de puntos
        marker=dict(
            color=colors,                      # Colores según churn
            size=8,                            # Tamaño de puntos
            opacity=0.7                        # Transparencia
        ),
        text=[f"Cliente {i+1}<br>Churn: {'Yes' if df['Churn'].iloc[i] else 'No'}" 
              for i in range(len(df))],        # Texto del hover
        hovertemplate='%{text}<extra></extra>' # Formato del hover
    ))
    
    # Configurar el layout
    fig.update_layout(
        title="PCA Analysis",
        xaxis_title=f"Principal Component 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)",
        yaxis_title=f"Principal Component 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)",
        height=500,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# =============================================================================
# 5. CONFIGURACIÓN DEL SERVIDOR
# =============================================================================
# Configurar el servidor para despliegue en producción
server = app.server

# Ejecutar la aplicación en modo desarrollo
if __name__ == '__main__':
    app.run_server(
        debug=True,        # Modo debug para desarrollo (recarga automática)
        host='0.0.0.0',    # Escuchar en todas las interfaces de red
        port=8050          # Puerto del servidor
    )
