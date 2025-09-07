# =============================================================================
# DASHBOARD DE BILLING OPERATIONS - CHARTER SPECTRUM
# =============================================================================
# Dashboard completo para operaciones de facturación con datos sintéticos
# 
# ESTRUCTURA:
# 1. Imports y configuración
# 2. Generación de datos sintéticos
# 3. Layout principal con múltiples pestañas
# 4. Callbacks para cada dashboard
# 5. Configuración del servidor
# =============================================================================

# =============================================================================
# 1. IMPORTS Y LIBRERÍAS NECESARIAS
# =============================================================================
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 2. CONFIGURACIÓN DE LA APLICACIÓN DASH
# =============================================================================
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ],
    suppress_callback_exceptions=True
)

app.title = "Billing Operations Dashboard - Charter Spectrum"

# =============================================================================
# 3. GENERACIÓN DE DATOS SINTÉTICOS
# =============================================================================

def generate_synthetic_data():
    """Genera datos sintéticos para todos los dashboards"""
    
    # Configurar semilla para reproducibilidad
    np.random.seed(42)
    random.seed(42)
    
    # Fechas para los últimos 30 días
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='H')
    
    # =====================================================================
    # DATOS DE FACTURACIÓN EN TIEMPO REAL
    # =====================================================================
    real_time_data = []
    for date in dates:
        # Simular variación por hora del día
        hour_factor = 1 + 0.5 * np.sin(2 * np.pi * date.hour / 24)
        
        real_time_data.append({
            'timestamp': date,
            'calls_volume': int(1000 + 500 * hour_factor + np.random.normal(0, 100)),
            'messages_volume': int(5000 + 2000 * hour_factor + np.random.normal(0, 500)),
            'data_volume_gb': round(100 + 50 * hour_factor + np.random.normal(0, 10), 2),
            'voice_revenue': round(5000 + 2000 * hour_factor + np.random.normal(0, 500), 2),
            'data_revenue': round(8000 + 3000 * hour_factor + np.random.normal(0, 800), 2),
            'total_revenue': round(13000 + 5000 * hour_factor + np.random.normal(0, 1000), 2)
        })
    
    real_time_df = pd.DataFrame(real_time_data)
    
    # =====================================================================
    # DATOS DE CLIENTES VIP
    # =====================================================================
    vip_customers = []
    customer_ids = [f'VIP_{i:03d}' for i in range(1, 21)]
    
    for customer_id in customer_ids:
        # Generar datos históricos para cada cliente VIP
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            vip_customers.append({
                'customer_id': customer_id,
                'date': date,
                'voice_usage_minutes': int(200 + np.random.normal(0, 50)),
                'data_usage_gb': round(10 + np.random.normal(0, 3), 2),
                'monthly_bill': round(150 + np.random.normal(0, 30), 2),
                'pending_amount': round(np.random.uniform(0, 50), 2),
                'service_level': random.choice(['Premium', 'Enterprise', 'Gold']),
                'satisfaction_score': round(np.random.uniform(7, 10), 1)
            })
    
    vip_df = pd.DataFrame(vip_customers)
    
    # =====================================================================
    # DATOS DE FACTURACIÓN POR DEPARTAMENTO
    # =====================================================================
    departments = ['Sales', 'Marketing', 'Engineering', 'Finance', 'HR', 'Operations', 'Customer Service']
    dept_data = []
    
    for dept in departments:
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            dept_data.append({
                'department': dept,
                'date': date,
                'billed_amount': round(5000 + np.random.normal(0, 1000), 2),
                'traffic_volume': int(1000 + np.random.normal(0, 200)),
                'active_users': int(50 + np.random.normal(0, 10)),
                'cost_per_user': round(50 + np.random.normal(0, 10), 2),
                'efficiency_score': round(np.random.uniform(0.7, 1.0), 2)
            })
    
    dept_df = pd.DataFrame(dept_data)
    
    # =====================================================================
    # DATOS DE FACTURACIÓN POR PRODUCTO
    # =====================================================================
    products = ['Internet 100Mbps', 'Internet 500Mbps', 'Internet 1Gbps', 'Cable TV Basic', 
                'Cable TV Premium', 'Phone Line', 'Mobile Plan', 'Bundle Package']
    product_data = []
    
    for product in products:
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            product_data.append({
                'product': product,
                'date': date,
                'billed_amount': round(10000 + np.random.normal(0, 2000), 2),
                'subscribers': int(500 + np.random.normal(0, 100)),
                'revenue_per_subscriber': round(80 + np.random.normal(0, 15), 2),
                'churn_rate': round(np.random.uniform(0.01, 0.05), 3),
                'profit_margin': round(np.random.uniform(0.2, 0.4), 2)
            })
    
    product_df = pd.DataFrame(product_data)
    
    # =====================================================================
    # DATOS DE QUEJAS Y RESOLUCIONES
    # =====================================================================
    complaint_types = ['Billing Error', 'Service Outage', 'Speed Issues', 'Customer Service', 
                      'Installation Problem', 'Equipment Issue', 'Contract Dispute']
    resolution_times = [1, 2, 3, 5, 7, 10, 15]  # días
    
    complaints_data = []
    for i in range(200):
        complaint_date = datetime.now() - timedelta(days=np.random.randint(1, 30))
        resolution_date = complaint_date + timedelta(days=random.choice(resolution_times))
        
        complaints_data.append({
            'complaint_id': f'COMP_{i:04d}',
            'complaint_date': complaint_date,
            'resolution_date': resolution_date,
            'complaint_type': random.choice(complaint_types),
            'priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'resolution_time_days': (resolution_date - complaint_date).days,
            'customer_satisfaction': random.choice([1, 2, 3, 4, 5]),
            'department': random.choice(departments),
            'status': random.choice(['Resolved', 'In Progress', 'Escalated'])
        })
    
    complaints_df = pd.DataFrame(complaints_data)
    
    # =====================================================================
    # DATOS DE ANÁLISIS DE CLIENTES
    # =====================================================================
    customer_data = []
    for i in range(1000):
        customer_data.append({
            'customer_id': f'CUST_{i:04d}',
            'age': np.random.randint(18, 80),
            'income_level': random.choice(['Low', 'Medium', 'High']),
            'tenure_months': np.random.randint(1, 120),
            'monthly_bill': round(50 + np.random.normal(0, 20), 2),
            'services_count': np.random.randint(1, 5),
            'churn_risk': round(np.random.uniform(0, 1), 2),
            'satisfaction_score': round(np.random.uniform(1, 10), 1),
            'payment_method': random.choice(['Credit Card', 'Bank Transfer', 'Check', 'Auto-Pay']),
            'region': random.choice(['Northeast', 'Southeast', 'Midwest', 'West'])
        })
    
    customer_df = pd.DataFrame(customer_data)
    
    # =====================================================================
    # DATOS DE ANÁLISIS DE RED
    # =====================================================================
    network_data = []
    for date in dates:
        network_data.append({
            'timestamp': date,
            'traffic_volume_gbps': round(10 + 5 * np.sin(2 * np.pi * date.hour / 24) + np.random.normal(0, 1), 2),
            'connection_speed_mbps': round(100 + np.random.normal(0, 10), 2),
            'latency_ms': round(20 + np.random.normal(0, 5), 2),
            'packet_loss_percent': round(np.random.uniform(0, 2), 3),
            'uptime_percent': round(99.5 + np.random.normal(0, 0.1), 2),
            'active_connections': int(50000 + np.random.normal(0, 5000)),
            'bandwidth_utilization': round(60 + 20 * np.sin(2 * np.pi * date.hour / 24) + np.random.normal(0, 5), 2)
        })
    
    network_df = pd.DataFrame(network_data)
    
    # =====================================================================
    # DATOS DE ANÁLISIS DE OPERACIONES
    # =====================================================================
    operations_data = []
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        operations_data.append({
            'date': date,
            'invoices_processed': int(1000 + np.random.normal(0, 100)),
            'processing_time_minutes': round(5 + np.random.normal(0, 1), 2),
            'error_rate_percent': round(np.random.uniform(0.1, 2.0), 2),
            'automation_rate_percent': round(85 + np.random.normal(0, 5), 2),
            'staff_productivity': round(np.random.uniform(0.8, 1.2), 2),
            'cost_per_invoice': round(2 + np.random.normal(0, 0.5), 2),
            'customer_satisfaction': round(np.random.uniform(7, 9), 1)
        })
    
    operations_df = pd.DataFrame(operations_data)
    
    return {
        'real_time': real_time_df,
        'vip_customers': vip_df,
        'departments': dept_df,
        'products': product_df,
        'complaints': complaints_df,
        'customers': customer_df,
        'network': network_df,
        'operations': operations_df
    }

# Generar datos
data = generate_synthetic_data()

# =============================================================================
# 4. LAYOUT PRINCIPAL
# =============================================================================

# =====================================================================
# PANTALLA DE CARGA
# =====================================================================
loading_screen = html.Div([
    # Imagen de fondo que ocupa toda la pantalla
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.95'
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
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H1([
                html.I(className="fas fa-chart-line me-3"),
                "Billing Operations Dashboard"
            ], className="text-primary fw-bold mb-0"),
            html.P("Charter Spectrum - Real-time Billing Analytics", 
                   className="text-muted mb-4")
        ], width=12)
    ], className="mb-4"),
    
    # Navegación con pestañas
    dbc.Row([
        dbc.Col([
            dbc.Tabs([
                dbc.Tab(label="Index", tab_id="index-tab", id="index-tab"),
                dbc.Tab(label="Real-time Billing", tab_id="real-time-tab", id="real-time-tab"),
                dbc.Tab(label="VIP Customers", tab_id="vip-tab", id="vip-tab"),
                dbc.Tab(label="Department Billing", tab_id="dept-tab", id="dept-tab"),
                dbc.Tab(label="Product Billing", tab_id="product-tab", id="product-tab"),
                dbc.Tab(label="Complaints & Resolutions", tab_id="complaints-tab", id="complaints-tab"),
                dbc.Tab(label="Customer Analysis", tab_id="customer-tab", id="customer-tab"),
                dbc.Tab(label="Network Analysis", tab_id="network-tab", id="network-tab"),
                dbc.Tab(label="Operations Analysis", tab_id="operations-tab", id="operations-tab")
            ], id="tabs", active_tab="index-tab"),
            html.Div(id="tab-content")
        ], width=12)
    ], className="mb-4"),
    
], fluid=True, className="py-4")

# =====================================================================
# CONTENIDO DE CADA PESTAÑA
# =====================================================================

# 1. REAL-TIME BILLING
real_time_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas principales
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-revenue', className="text-primary fw-bold"),
                        html.P("Total Revenue (24h)", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='calls-volume', className="text-success fw-bold"),
                        html.P("Calls Volume", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='data-volume', className="text-info fw-bold"),
                        html.P("Data Volume (GB)", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='messages-volume', className="text-warning fw-bold"),
                        html.P("Messages Volume", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2"),
                            "Revenue Trends (Last 24 Hours)"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='revenue-trends')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Service Usage by Hour"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='service-usage')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Revenue Distribution"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='revenue-distribution')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 2. VIP CUSTOMERS
vip_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas VIP
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-vip', className="text-primary fw-bold"),
                        html.P("Total VIP Customers", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-vip-bill', className="text-success fw-bold"),
                        html.P("Avg VIP Bill", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='vip-satisfaction', className="text-info fw-bold"),
                        html.P("VIP Satisfaction", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='pending-vip-amount', className="text-warning fw-bold"),
                        html.P("Pending VIP Amount", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos VIP
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-users me-2"),
                            "VIP Customer Usage Trends"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='vip-usage-trends')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "VIP Customer Performance"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='vip-performance')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "VIP Service Level Distribution"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='vip-service-levels')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 3. DEPARTMENT BILLING
dept_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas de departamentos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-dept-billed', className="text-primary fw-bold"),
                        html.P("Total Billed by Depts", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-dept-efficiency', className="text-success fw-bold"),
                        html.P("Avg Dept Efficiency", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-dept-users', className="text-info fw-bold"),
                        html.P("Total Active Users", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-cost-per-user', className="text-warning fw-bold"),
                        html.P("Avg Cost per User", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos de departamentos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-building me-2"),
                            "Department Billing Trends"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='dept-billing-trends')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Department Performance Comparison"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='dept-performance')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Department Efficiency Distribution"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='dept-efficiency')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 4. PRODUCT BILLING
product_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas de productos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-product-revenue', className="text-primary fw-bold"),
                        html.P("Total Product Revenue", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-subscribers', className="text-success fw-bold"),
                        html.P("Total Subscribers", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-churn-rate', className="text-info fw-bold"),
                        html.P("Avg Churn Rate", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-profit-margin', className="text-warning fw-bold"),
                        html.P("Avg Profit Margin", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos de productos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2"),
                            "Product Revenue Trends"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='product-revenue-trends')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Product Performance Comparison"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='product-performance')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Revenue by Product Category"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='product-revenue-distribution')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2"),
                            "Churn Rate Analysis by Product"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='product-churn-analysis')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 5. COMPLAINTS & RESOLUTIONS
complaints_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas de quejas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-complaints', className="text-primary fw-bold"),
                        html.P("Total Complaints", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-resolution-time', className="text-success fw-bold"),
                        html.P("Avg Resolution Time", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-satisfaction', className="text-info fw-bold"),
                        html.P("Avg Satisfaction", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='resolution-rate', className="text-warning fw-bold"),
                        html.P("Resolution Rate", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos de quejas
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2"),
                            "Complaints Timeline"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='complaints-timeline')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Complaints by Type and Priority"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='complaints-by-type')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Resolution Time Distribution"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='resolution-time-distribution')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2"),
                            "Department Performance in Complaints"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='department-complaints-performance')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 6. CUSTOMER ANALYSIS
customer_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas de clientes
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-customers', className="text-primary fw-bold"),
                        html.P("Total Customers", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-monthly-bill', className="text-success fw-bold"),
                        html.P("Avg Monthly Bill", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-satisfaction-score', className="text-info fw-bold"),
                        html.P("Avg Satisfaction", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='high-churn-risk', className="text-warning fw-bold"),
                        html.P("High Churn Risk", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos de clientes
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2"),
                            "Customer Demographics Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='customer-demographics')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Customer Behavior Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='customer-behavior')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Customer Segmentation"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='customer-segmentation')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2"),
                            "Churn Risk Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='churn-risk-analysis')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 7. NETWORK ANALYSIS
network_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas de red
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-traffic-volume', className="text-primary fw-bold"),
                        html.P("Avg Traffic Volume", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-connection-speed', className="text-success fw-bold"),
                        html.P("Avg Connection Speed", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-uptime', className="text-info fw-bold"),
                        html.P("Avg Uptime", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-latency', className="text-warning fw-bold"),
                        html.P("Avg Latency", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos de red
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2"),
                            "Network Performance Trends"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='network-performance-trends')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Network Metrics Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='network-metrics-analysis')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Bandwidth Utilization"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='bandwidth-utilization')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2"),
                            "Network Health Dashboard"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='network-health-dashboard')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# 8. OPERATIONS ANALYSIS
operations_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Métricas de operaciones
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-invoices-processed', className="text-primary fw-bold"),
                        html.P("Total Invoices Processed", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-processing-time', className="text-success fw-bold"),
                        html.P("Avg Processing Time", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='automation-rate', className="text-info fw-bold"),
                        html.P("Automation Rate", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='error-rate', className="text-warning fw-bold"),
                        html.P("Error Rate", className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Gráficos de operaciones
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-line me-2"),
                            "Operations Performance Trends"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='operations-performance-trends')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-bar me-2"),
                            "Operations Efficiency Analysis"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='operations-efficiency-analysis')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-pie me-2"),
                            "Cost Analysis by Operation"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='cost-analysis')
                    ])
                ], className="border-0 shadow-sm")
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5([
                            html.I(className="fas fa-chart-area me-2"),
                            "Operations Health Dashboard"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        dcc.Graph(id='operations-health-dashboard')
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ], className="mb-4")
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# INDEX PAGE - DASHBOARD GUIDE
index_content = html.Div([
    # Imagen de fondo
    html.Img(
        src="/assets/Enterprise_Hero_0.jpg",
        style={
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'width': '100vw',
            'height': '100vh',
            'objectFit': 'cover',
            'zIndex': '-1',
            'opacity': '0.15'
        }
    ),
    # Contenido
    dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1([
                    html.I(className="fas fa-book me-3"),
                    "Billing Operations Dashboard Guide"
                ], className="text-primary fw-bold mb-3"),
                html.P("Complete guide to understanding all dashboard sections, metrics, and visualizations", 
                       className="text-muted mb-4 fs-5")
            ], width=12)
        ], className="mb-4"),
        
        # Overview
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-info-circle me-2"),
                            "Dashboard Overview"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.P([
                            "This comprehensive dashboard provides real-time insights into Charter Spectrum's billing operations. ",
                            "It includes 8 main sections covering everything from real-time billing metrics to network performance analysis. ",
                            "Each section contains interactive visualizations and key performance indicators (KPIs) to help you ",
                            "make data-driven decisions and optimize business operations."
                        ], className="mb-3"),
                        html.H6("Key Features:", className="fw-bold"),
                        html.Ul([
                            html.Li("Real-time data visualization with interactive charts"),
                            html.Li("Comprehensive customer and product analysis"),
                            html.Li("Network performance monitoring"),
                            html.Li("Operations efficiency tracking"),
                            html.Li("Automated reporting and trend analysis")
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 1: Real-time Billing
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-chart-line me-2"),
                            "1. Real-time Billing"
                        ], className="mb-0 text-primary")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Monitor live billing operations, revenue generation, and service usage patterns in real-time."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total Revenue (24h) - Total revenue generated in the last 24 hours"),
                            html.Li("Calls Volume - Number of voice calls processed"),
                            html.Li("Data Volume (GB) - Amount of data transferred"),
                            html.Li("Messages Volume - Number of text messages sent")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Revenue Trends: "),
                                "Line chart showing revenue trends over the last 24 hours, including voice and data revenue breakdown"
                            ]),
                            html.Li([
                                html.Strong("Service Usage by Hour: "),
                                "Four subplots displaying calls, messages, data usage, and revenue per hour"
                            ]),
                            html.Li([
                                html.Strong("Revenue Distribution: "),
                                "Donut chart showing the proportion of voice vs data revenue"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 2: VIP Customers
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-crown me-2"),
                            "2. VIP Customers"
                        ], className="mb-0 text-success")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Track and analyze high-value customers to ensure premium service delivery and retention."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total VIP Customers - Number of premium customers"),
                            html.Li("Avg VIP Bill - Average monthly bill for VIP customers"),
                            html.Li("VIP Satisfaction - Average satisfaction score"),
                            html.Li("Pending VIP Amount - Outstanding amounts from VIP customers")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("VIP Customer Usage Trends: "),
                                "Line chart showing voice usage, data usage, and monthly bills over time"
                            ]),
                            html.Li([
                                html.Strong("VIP Customer Performance: "),
                                "Bar chart ranking top 10 VIP customers by monthly bill amount"
                            ]),
                            html.Li([
                                html.Strong("VIP Service Level Distribution: "),
                                "Donut chart showing distribution of customers by service level (Premium, Enterprise, Gold)"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 3: Department Billing
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-building me-2"),
                            "3. Department Billing"
                        ], className="mb-0 text-info")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Analyze billing performance across different departments to optimize resource allocation and efficiency."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total Billed by Depts - Total amount billed across all departments"),
                            html.Li("Avg Dept Efficiency - Average efficiency score across departments"),
                            html.Li("Total Active Users - Total number of active users across departments"),
                            html.Li("Avg Cost per User - Average cost per user across departments")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Department Billing Trends: "),
                                "Line chart showing billing trends for each department over 30 days"
                            ]),
                            html.Li([
                                html.Strong("Department Performance Comparison: "),
                                "Grouped bar chart comparing billed amounts and active users by department"
                            ]),
                            html.Li([
                                html.Strong("Department Efficiency Distribution: "),
                                "Donut chart showing efficiency scores by department"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 4: Product Billing
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-box me-2"),
                            "4. Product Billing"
                        ], className="mb-0 text-warning")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Evaluate product performance, profitability, and customer adoption to optimize product strategy."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total Product Revenue - Total revenue from all products"),
                            html.Li("Total Subscribers - Total number of subscribers across products"),
                            html.Li("Avg Churn Rate - Average customer churn rate"),
                            html.Li("Avg Profit Margin - Average profit margin across products")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Product Revenue Trends: "),
                                "Line chart showing revenue trends for each product over 30 days"
                            ]),
                            html.Li([
                                html.Strong("Product Performance Comparison: "),
                                "Grouped bar chart comparing revenue and subscribers by product"
                            ]),
                            html.Li([
                                html.Strong("Revenue by Product Category: "),
                                "Donut chart showing revenue distribution by product category (Internet, Cable TV, Phone, etc.)"
                            ]),
                            html.Li([
                                html.Strong("Churn Rate Analysis: "),
                                "Four subplots showing churn rate, profit margin, revenue per subscriber, and subscriber distribution by product"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 5: Complaints & Resolutions
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-exclamation-triangle me-2"),
                            "5. Complaints & Resolutions"
                        ], className="mb-0 text-danger")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Monitor customer complaints, resolution times, and service quality to improve customer satisfaction."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total Complaints - Total number of complaints received"),
                            html.Li("Avg Resolution Time - Average time to resolve complaints"),
                            html.Li("Avg Satisfaction - Average customer satisfaction score"),
                            html.Li("Resolution Rate - Percentage of complaints successfully resolved")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Complaints Timeline: "),
                                "Line chart comparing complaints vs resolutions over time"
                            ]),
                            html.Li([
                                html.Strong("Complaints by Type and Priority: "),
                                "Stacked bar chart showing complaints by type and priority level"
                            ]),
                            html.Li([
                                html.Strong("Resolution Time Distribution: "),
                                "Donut chart showing distribution of resolution times (Same Day, 1-3 Days, etc.)"
                            ]),
                            html.Li([
                                html.Strong("Department Performance in Complaints: "),
                                "Four subplots showing total complaints, resolution times, satisfaction, and performance correlation by department"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 6: Customer Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-users me-2"),
                            "6. Customer Analysis"
                        ], className="mb-0 text-secondary")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Analyze customer demographics, behavior patterns, and churn risk to improve retention strategies."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total Customers - Total number of customers in the database"),
                            html.Li("Avg Monthly Bill - Average monthly bill across all customers"),
                            html.Li("Avg Satisfaction - Average customer satisfaction score"),
                            html.Li("High Churn Risk - Number of customers with high churn risk (>70%)")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Customer Demographics Analysis: "),
                                "Four subplots showing age distribution, income levels, tenure, and regional distribution"
                            ]),
                            html.Li([
                                html.Strong("Customer Behavior Analysis: "),
                                "Four subplots showing monthly bill distribution, services count, payment methods, and satisfaction scores"
                            ]),
                            html.Li([
                                html.Strong("Customer Segmentation: "),
                                "Donut chart showing customer segments by value and satisfaction (High Value Satisfied, High Value At Risk, etc.)"
                            ]),
                            html.Li([
                                html.Strong("Churn Risk Analysis: "),
                                "Four subplots showing churn risk distribution and correlations with monthly bill, tenure, and satisfaction"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 7: Network Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-network-wired me-2"),
                            "7. Network Analysis"
                        ], className="mb-0 text-dark")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Monitor network performance, identify bottlenecks, and optimize network resources for better service quality."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Avg Traffic Volume - Average network traffic volume in Gbps"),
                            html.Li("Avg Connection Speed - Average connection speed in Mbps"),
                            html.Li("Avg Uptime - Average network uptime percentage"),
                            html.Li("Avg Latency - Average network latency in milliseconds")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Network Performance Trends: "),
                                "Multi-line chart showing traffic volume, connection speed, and latency over 24 hours"
                            ]),
                            html.Li([
                                html.Strong("Network Metrics Analysis: "),
                                "Four subplots showing active connections, packet loss, bandwidth utilization, and uptime"
                            ]),
                            html.Li([
                                html.Strong("Bandwidth Utilization: "),
                                "Donut chart showing bandwidth utilization categories (Low, Medium, High, Critical)"
                            ]),
                            html.Li([
                                html.Strong("Network Health Dashboard: "),
                                "Four subplots showing network health score, performance by time of day, and correlation analyses"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Section 8: Operations Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H4([
                            html.I(className="fas fa-cogs me-2"),
                            "8. Operations Analysis"
                        ], className="mb-0 text-muted")
                    ]),
                    dbc.CardBody([
                        html.H6("Purpose:", className="fw-bold"),
                        html.P("Analyze operational efficiency, identify process improvements, and optimize resource allocation."),
                        
                        html.H6("Key Metrics:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li("Total Invoices Processed - Total number of invoices processed"),
                            html.Li("Avg Processing Time - Average time to process invoices"),
                            html.Li("Automation Rate - Percentage of automated processes"),
                            html.Li("Error Rate - Percentage of processing errors")
                        ]),
                        
                        html.H6("Charts & Visualizations:", className="fw-bold mt-3"),
                        html.Ul([
                            html.Li([
                                html.Strong("Operations Performance Trends: "),
                                "Multi-line chart showing invoices processed, processing time, and automation rate over 30 days"
                            ]),
                            html.Li([
                                html.Strong("Operations Efficiency Analysis: "),
                                "Four subplots showing staff productivity, error rates, cost per invoice, and customer satisfaction"
                            ]),
                            html.Li([
                                html.Strong("Cost Analysis by Operation: "),
                                "Donut chart showing cost categories (Low, Medium, High, Very High)"
                            ]),
                            html.Li([
                                html.Strong("Operations Health Dashboard: "),
                                "Four subplots showing operations health score and correlation analyses between efficiency metrics"
                            ])
                        ])
                    ])
                ], className="border-0 shadow-sm mb-4")
            ], width=12)
        ]),
        
        # Footer
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("How to Use This Dashboard:", className="fw-bold"),
                        html.Ul([
                            html.Li("Navigate between tabs using the tab navigation at the top"),
                            html.Li("Hover over charts for detailed information"),
                            html.Li("Use the interactive features to explore data trends"),
                            html.Li("Monitor key metrics for quick decision-making"),
                            html.Li("Export data or screenshots as needed for reporting")
                        ]),
                        html.Hr(),
                        html.P([
                            html.I(className="fas fa-info-circle me-2"),
                            "All data is synthetic and for demonstration purposes. In a real environment, ",
                            "this dashboard would connect to live data sources and update in real-time."
                        ], className="text-muted mb-0")
                    ])
                ], className="border-0 shadow-sm")
            ], width=12)
        ])
        
    ], fluid=True, className="py-4", style={'backgroundColor': 'rgba(255, 255, 255, 0.95)', 'borderRadius': '10px', 'marginTop': '20px', 'marginBottom': '20px'})
])

# =====================================================================
# LAYOUT PRINCIPAL CON SISTEMA DE CARGA

# =====================================================================
# LAYOUT PRINCIPAL CON SISTEMA DE CARGA
# =====================================================================
app.layout = html.Div([
    # Store para controlar la visibilidad
    dcc.Store(id='loading-state', data={'show_loading': True}),
    
    # Intervalo para la animación de puntos suspensivos
    dcc.Interval(
        id='loading-interval',
        interval=500,
        n_intervals=0,
        disabled=False
    ),
    
    # Intervalo para cambiar de pantalla de carga al dashboard
    dcc.Interval(
        id='dashboard-interval',
        interval=2000,
        n_intervals=0,
        disabled=False
    ),
    
    # Contenedor principal que cambia entre loading y dashboard
    html.Div(id='main-content')
])

# =============================================================================
# 5. CALLBACKS
# =============================================================================

# Callback para animación de puntos suspensivos
@callback(
    Output('loading-dots', 'children'),
    Input('loading-interval', 'n_intervals')
)
def update_loading_dots(n):
    dots = "." * ((n % 4) + 1)
    return dots

# Callback para cambio de pantalla de carga al dashboard
@callback(
    Output('main-content', 'children'),
    Output('loading-interval', 'disabled'),
    Output('dashboard-interval', 'disabled'),
    Input('dashboard-interval', 'n_intervals'),
    Input('loading-state', 'data')
)
def switch_to_dashboard(n_intervals, loading_data):
    if n_intervals >= 2:
        return main_dashboard, True, True
    else:
        return loading_screen, False, False

# Callback para navegación entre pestañas
@callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
)
def switch_tab(active_tab):
    if active_tab == "index-tab":
        return index_content
    elif active_tab == "real-time-tab":
        return real_time_content
    elif active_tab == "vip-tab":
        return vip_content
    elif active_tab == "dept-tab":
        return dept_content
    elif active_tab == "product-tab":
        return product_content
    elif active_tab == "complaints-tab":
        return complaints_content
    elif active_tab == "customer-tab":
        return customer_content
    elif active_tab == "network-tab":
        return network_content
    elif active_tab == "operations-tab":
        return operations_content
    else:
        return index_content

# Callbacks para Real-time Billing
@callback(
    [Output('total-revenue', 'children'),
     Output('calls-volume', 'children'),
     Output('data-volume', 'children'),
     Output('messages-volume', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_real_time_metrics(active_tab):
    if active_tab != "real-time-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    # Obtener datos de las últimas 24 horas
    last_24h = data['real_time'].tail(24)
    
    total_revenue = f"${last_24h['total_revenue'].sum():,.0f}"
    calls_volume = f"{last_24h['calls_volume'].sum():,}"
    data_volume = f"{last_24h['data_volume_gb'].sum():,.0f}"
    messages_volume = f"{last_24h['messages_volume'].sum():,}"
    
    return total_revenue, calls_volume, data_volume, messages_volume

@callback(
    Output('revenue-trends', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_revenue_trends(active_tab):
    if active_tab != "real-time-tab":
        return go.Figure()
    
    df = data['real_time'].tail(24)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['total_revenue'],
        mode='lines+markers',
        name='Total Revenue',
        line=dict(color='#007bff', width=3),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['voice_revenue'],
        mode='lines+markers',
        name='Voice Revenue',
        line=dict(color='#28a745', width=2),
        marker=dict(size=4)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['data_revenue'],
        mode='lines+markers',
        name='Data Revenue',
        line=dict(color='#ffc107', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title="Revenue Trends - Last 24 Hours",
        xaxis_title="Time",
        yaxis_title="Revenue ($)",
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('service-usage', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_service_usage(active_tab):
    if active_tab != "real-time-tab":
        return go.Figure()
    
    df = data['real_time'].tail(24)
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Calls Volume', 'Messages Volume', 'Data Volume', 'Revenue per Hour'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Calls Volume
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['calls_volume'], name='Calls', marker_color='#007bff'),
        row=1, col=1
    )
    
    # Messages Volume
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['messages_volume'], name='Messages', marker_color='#28a745'),
        row=1, col=2
    )
    
    # Data Volume
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['data_volume_gb'], name='Data (GB)', marker_color='#ffc107'),
        row=2, col=1
    )
    
    # Revenue per Hour
    fig.add_trace(
        go.Bar(x=df['timestamp'], y=df['total_revenue'], name='Revenue ($)', marker_color='#dc3545'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('revenue-distribution', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_revenue_distribution(active_tab):
    if active_tab != "real-time-tab":
        return go.Figure()
    
    df = data['real_time'].tail(24)
    
    voice_total = df['voice_revenue'].sum()
    data_total = df['data_revenue'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=['Voice Revenue', 'Data Revenue'],
        values=[voice_total, data_total],
        hole=0.4,
        marker_colors=['#28a745', '#ffc107'],
        textinfo='label+percent',
        textfont_size=14
    )])
    
    fig.update_layout(
        title="Revenue Distribution - Last 24 Hours",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Callbacks para VIP Customers
@callback(
    [Output('total-vip', 'children'),
     Output('avg-vip-bill', 'children'),
     Output('vip-satisfaction', 'children'),
     Output('pending-vip-amount', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_vip_metrics(active_tab):
    if active_tab != "vip-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['vip_customers']
    
    total_vip = len(df['customer_id'].unique())
    avg_bill = f"${df['monthly_bill'].mean():.0f}"
    avg_satisfaction = f"{df['satisfaction_score'].mean():.1f}/10"
    pending_amount = f"${df['pending_amount'].sum():,.0f}"
    
    return total_vip, avg_bill, avg_satisfaction, pending_amount

@callback(
    Output('vip-usage-trends', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_vip_usage_trends(active_tab):
    if active_tab != "vip-tab":
        return go.Figure()
    
    df = data['vip_customers']
    
    # Agrupar por fecha
    daily_usage = df.groupby('date').agg({
        'voice_usage_minutes': 'mean',
        'data_usage_gb': 'mean',
        'monthly_bill': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_usage['date'],
        y=daily_usage['voice_usage_minutes'],
        mode='lines+markers',
        name='Voice Usage (min)',
        line=dict(color='#007bff', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=daily_usage['date'],
        y=daily_usage['data_usage_gb'],
        mode='lines+markers',
        name='Data Usage (GB)',
        line=dict(color='#28a745', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="VIP Customer Usage Trends",
        xaxis_title="Date",
        yaxis_title="Voice Usage (minutes)",
        yaxis2=dict(title="Data Usage (GB)", overlaying='y', side='right'),
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('vip-performance', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_vip_performance(active_tab):
    if active_tab != "vip-tab":
        return go.Figure()
    
    df = data['vip_customers']
    
    # Obtener los últimos datos de cada cliente VIP
    latest_data = df.groupby('customer_id').last().reset_index()
    
    # Top 10 clientes por factura mensual
    top_customers = latest_data.nlargest(10, 'monthly_bill')
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=top_customers['customer_id'],
        y=top_customers['monthly_bill'],
        name='Monthly Bill ($)',
        marker_color='#007bff',
        text=top_customers['monthly_bill'].round(0),
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Top 10 VIP Customers by Monthly Bill",
        xaxis_title="Customer ID",
        yaxis_title="Monthly Bill ($)",
        height=400,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis={'categoryorder':'total descending'}
    )
    
    return fig

@callback(
    Output('vip-service-levels', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_vip_service_levels(active_tab):
    if active_tab != "vip-tab":
        return go.Figure()
    
    df = data['vip_customers']
    
    # Obtener los últimos datos de cada cliente VIP
    latest_data = df.groupby('customer_id').last().reset_index()
    
    # Contar clientes por nivel de servicio
    service_level_counts = latest_data['service_level'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=service_level_counts.index,
        values=service_level_counts.values,
        hole=0.4,
        marker_colors=['#007bff', '#28a745', '#ffc107'],
        textinfo='label+percent+value',
        textfont_size=14
    )])
    
    fig.update_layout(
        title="VIP Customers by Service Level",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Callbacks para Department Billing
@callback(
    [Output('total-dept-billed', 'children'),
     Output('avg-dept-efficiency', 'children'),
     Output('total-dept-users', 'children'),
     Output('avg-cost-per-user', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_dept_metrics(active_tab):
    if active_tab != "dept-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['departments']
    
    total_billed = f"${df['billed_amount'].sum():,.0f}"
    avg_efficiency = f"{df['efficiency_score'].mean():.1%}"
    total_users = f"{df['active_users'].sum():,}"
    avg_cost = f"${df['cost_per_user'].mean():.0f}"
    
    return total_billed, avg_efficiency, total_users, avg_cost

@callback(
    Output('dept-billing-trends', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_dept_billing_trends(active_tab):
    if active_tab != "dept-tab":
        return go.Figure()
    
    df = data['departments']
    
    # Agrupar por departamento y fecha
    dept_trends = df.groupby(['department', 'date'])['billed_amount'].sum().reset_index()
    
    fig = go.Figure()
    
    # Agregar una línea por cada departamento
    departments = df['department'].unique()
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14', '#20c997']
    
    for i, dept in enumerate(departments):
        dept_data = dept_trends[dept_trends['department'] == dept]
        fig.add_trace(go.Scatter(
            x=dept_data['date'],
            y=dept_data['billed_amount'],
            mode='lines+markers',
            name=dept,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=4)
        ))
    
    fig.update_layout(
        title="Department Billing Trends - Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Billed Amount ($)",
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('dept-performance', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_dept_performance(active_tab):
    if active_tab != "dept-tab":
        return go.Figure()
    
    df = data['departments']
    
    # Obtener los últimos datos de cada departamento
    latest_data = df.groupby('department').last().reset_index()
    
    fig = go.Figure()
    
    # Gráfico de barras para facturación total
    fig.add_trace(go.Bar(
        x=latest_data['department'],
        y=latest_data['billed_amount'],
        name='Billed Amount ($)',
        marker_color='#007bff',
        text=latest_data['billed_amount'].round(0),
        textposition='auto'
    ))
    
    # Gráfico de barras para usuarios activos (eje secundario)
    fig.add_trace(go.Bar(
        x=latest_data['department'],
        y=latest_data['active_users'],
        name='Active Users',
        marker_color='#28a745',
        text=latest_data['active_users'],
        textposition='auto',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Department Performance Comparison",
        xaxis_title="Department",
        yaxis_title="Billed Amount ($)",
        yaxis2=dict(title="Active Users", overlaying='y', side='right'),
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50),
        barmode='group'
    )
    
    return fig

@callback(
    Output('dept-efficiency', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_dept_efficiency(active_tab):
    if active_tab != "dept-tab":
        return go.Figure()
    
    df = data['departments']
    
    # Obtener los últimos datos de cada departamento
    latest_data = df.groupby('department').last().reset_index()
    
    # Calcular eficiencia promedio por departamento
    dept_efficiency = latest_data.groupby('department')['efficiency_score'].mean().reset_index()
    
    fig = go.Figure(data=[go.Pie(
        labels=dept_efficiency['department'],
        values=dept_efficiency['efficiency_score'],
        hole=0.4,
        marker_colors=['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14', '#20c997'],
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Department Efficiency Distribution",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Callbacks para Product Billing
@callback(
    [Output('total-product-revenue', 'children'),
     Output('total-subscribers', 'children'),
     Output('avg-churn-rate', 'children'),
     Output('avg-profit-margin', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_product_metrics(active_tab):
    if active_tab != "product-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['products']
    
    total_revenue = f"${df['billed_amount'].sum():,.0f}"
    total_subs = f"{df['subscribers'].sum():,}"
    avg_churn = f"{df['churn_rate'].mean():.1%}"
    avg_margin = f"{df['profit_margin'].mean():.1%}"
    
    return total_revenue, total_subs, avg_churn, avg_margin

@callback(
    Output('product-revenue-trends', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_product_revenue_trends(active_tab):
    if active_tab != "product-tab":
        return go.Figure()
    
    df = data['products']
    
    # Agrupar por producto y fecha
    product_trends = df.groupby(['product', 'date'])['billed_amount'].sum().reset_index()
    
    fig = go.Figure()
    
    # Agregar una línea por cada producto
    products = df['product'].unique()
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14', '#20c997', '#e83e8c']
    
    for i, product in enumerate(products):
        product_data = product_trends[product_trends['product'] == product]
        fig.add_trace(go.Scatter(
            x=product_data['date'],
            y=product_data['billed_amount'],
            mode='lines+markers',
            name=product,
            line=dict(color=colors[i % len(colors)], width=2),
            marker=dict(size=4)
        ))
    
    fig.update_layout(
        title="Product Revenue Trends - Last 30 Days",
        xaxis_title="Date",
        yaxis_title="Revenue ($)",
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('product-performance', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_product_performance(active_tab):
    if active_tab != "product-tab":
        return go.Figure()
    
    df = data['products']
    
    # Obtener los últimos datos de cada producto
    latest_data = df.groupby('product').last().reset_index()
    
    fig = go.Figure()
    
    # Gráfico de barras para facturación total
    fig.add_trace(go.Bar(
        x=latest_data['product'],
        y=latest_data['billed_amount'],
        name='Revenue ($)',
        marker_color='#007bff',
        text=latest_data['billed_amount'].round(0),
        textposition='auto'
    ))
    
    # Gráfico de barras para suscriptores (eje secundario)
    fig.add_trace(go.Bar(
        x=latest_data['product'],
        y=latest_data['subscribers'],
        name='Subscribers',
        marker_color='#28a745',
        text=latest_data['subscribers'],
        textposition='auto',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Product Performance Comparison",
        xaxis_title="Product",
        yaxis_title="Revenue ($)",
        yaxis2=dict(title="Subscribers", overlaying='y', side='right'),
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50),
        barmode='group'
    )
    
    return fig

@callback(
    Output('product-revenue-distribution', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_product_revenue_distribution(active_tab):
    if active_tab != "product-tab":
        return go.Figure()
    
    df = data['products']
    
    # Obtener los últimos datos de cada producto
    latest_data = df.groupby('product').last().reset_index()
    
    # Categorizar productos
    def categorize_product(product_name):
        if 'Internet' in product_name:
            return 'Internet Services'
        elif 'Cable TV' in product_name:
            return 'Cable TV'
        elif 'Phone' in product_name:
            return 'Phone Services'
        elif 'Mobile' in product_name:
            return 'Mobile Services'
        elif 'Bundle' in product_name:
            return 'Bundle Packages'
        else:
            return 'Other Services'
    
    latest_data['category'] = latest_data['product'].apply(categorize_product)
    
    # Agrupar por categoría
    category_revenue = latest_data.groupby('category')['billed_amount'].sum().reset_index()
    
    fig = go.Figure(data=[go.Pie(
        labels=category_revenue['category'],
        values=category_revenue['billed_amount'],
        hole=0.4,
        marker_colors=['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'],
        textinfo='label+percent+value',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Revenue by Product Category",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('product-churn-analysis', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_product_churn_analysis(active_tab):
    if active_tab != "product-tab":
        return go.Figure()
    
    df = data['products']
    
    # Obtener los últimos datos de cada producto
    latest_data = df.groupby('product').last().reset_index()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Churn Rate by Product', 'Profit Margin by Product', 
                       'Revenue per Subscriber', 'Subscriber Distribution'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Churn Rate
    fig.add_trace(
        go.Bar(x=latest_data['product'], y=latest_data['churn_rate'], 
               name='Churn Rate', marker_color='#dc3545'),
        row=1, col=1
    )
    
    # Profit Margin
    fig.add_trace(
        go.Bar(x=latest_data['product'], y=latest_data['profit_margin'], 
               name='Profit Margin', marker_color='#28a745'),
        row=1, col=2
    )
    
    # Revenue per Subscriber
    fig.add_trace(
        go.Bar(x=latest_data['product'], y=latest_data['revenue_per_subscriber'], 
               name='Revenue/Subscriber', marker_color='#007bff'),
        row=2, col=1
    )
    
    # Subscriber Distribution
    fig.add_trace(
        go.Bar(x=latest_data['product'], y=latest_data['subscribers'], 
               name='Subscribers', marker_color='#ffc107'),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Callbacks para Complaints & Resolutions
@callback(
    [Output('total-complaints', 'children'),
     Output('avg-resolution-time', 'children'),
     Output('avg-satisfaction', 'children'),
     Output('resolution-rate', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_complaints_metrics(active_tab):
    if active_tab != "complaints-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['complaints']
    
    total_complaints = len(df)
    avg_resolution_time = f"{df['resolution_time_days'].mean():.1f} days"
    avg_satisfaction = f"{df['customer_satisfaction'].mean():.1f}/5"
    resolution_rate = f"{(len(df[df['status'] == 'Resolved']) / len(df)) * 100:.1f}%"
    
    return total_complaints, avg_resolution_time, avg_satisfaction, resolution_rate

@callback(
    Output('complaints-timeline', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_complaints_timeline(active_tab):
    if active_tab != "complaints-tab":
        return go.Figure()
    
    df = data['complaints']
    
    # Agrupar quejas por fecha
    daily_complaints = df.groupby(df['complaint_date'].dt.date).size().reset_index()
    daily_complaints.columns = ['date', 'complaints_count']
    
    # Agrupar resoluciones por fecha
    daily_resolutions = df[df['status'] == 'Resolved'].groupby(df['resolution_date'].dt.date).size().reset_index()
    daily_resolutions.columns = ['date', 'resolutions_count']
    
    fig = go.Figure()
    
    # Quejas diarias
    fig.add_trace(go.Scatter(
        x=daily_complaints['date'],
        y=daily_complaints['complaints_count'],
        mode='lines+markers',
        name='Complaints',
        line=dict(color='#dc3545', width=3),
        marker=dict(size=6)
    ))
    
    # Resoluciones diarias
    fig.add_trace(go.Scatter(
        x=daily_resolutions['date'],
        y=daily_resolutions['resolutions_count'],
        mode='lines+markers',
        name='Resolutions',
        line=dict(color='#28a745', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Complaints vs Resolutions Timeline",
        xaxis_title="Date",
        yaxis_title="Count",
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('complaints-by-type', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_complaints_by_type(active_tab):
    if active_tab != "complaints-tab":
        return go.Figure()
    
    df = data['complaints']
    
    # Crear tabla cruzada de tipo de queja vs prioridad
    complaint_cross = pd.crosstab(df['complaint_type'], df['priority'])
    
    fig = go.Figure()
    
    # Agregar barras para cada prioridad
    priorities = ['Low', 'Medium', 'High', 'Critical']
    colors = ['#28a745', '#ffc107', '#fd7e14', '#dc3545']
    
    for i, priority in enumerate(priorities):
        if priority in complaint_cross.columns:
            fig.add_trace(go.Bar(
                x=complaint_cross.index,
                y=complaint_cross[priority],
                name=priority,
                marker_color=colors[i],
                text=complaint_cross[priority],
                textposition='auto'
            ))
    
    fig.update_layout(
        title="Complaints by Type and Priority",
        xaxis_title="Complaint Type",
        yaxis_title="Number of Complaints",
        height=400,
        showlegend=True,
        margin=dict(t=50, b=50, l=50, r=50),
        barmode='stack'
    )
    
    return fig

@callback(
    Output('resolution-time-distribution', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_resolution_time_distribution(active_tab):
    if active_tab != "complaints-tab":
        return go.Figure()
    
    df = data['complaints']
    
    # Categorizar tiempos de resolución
    def categorize_resolution_time(days):
        if days <= 1:
            return 'Same Day'
        elif days <= 3:
            return '1-3 Days'
        elif days <= 7:
            return '4-7 Days'
        elif days <= 14:
            return '8-14 Days'
        else:
            return '15+ Days'
    
    df['resolution_category'] = df['resolution_time_days'].apply(categorize_resolution_time)
    resolution_dist = df['resolution_category'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=resolution_dist.index,
        values=resolution_dist.values,
        hole=0.4,
        marker_colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545', '#6c757d'],
        textinfo='label+percent+value',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Resolution Time Distribution",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('department-complaints-performance', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_department_complaints_performance(active_tab):
    if active_tab != "complaints-tab":
        return go.Figure()
    
    df = data['complaints']
    
    # Calcular métricas por departamento
    dept_metrics = df.groupby('department').agg({
        'complaint_id': 'count',
        'resolution_time_days': 'mean',
        'customer_satisfaction': 'mean'
    }).reset_index()
    
    dept_metrics.columns = ['department', 'total_complaints', 'avg_resolution_time', 'avg_satisfaction']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Total Complaints by Department', 'Avg Resolution Time by Department',
                       'Avg Customer Satisfaction by Department', 'Complaints vs Resolution Time'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Total complaints
    fig.add_trace(
        go.Bar(x=dept_metrics['department'], y=dept_metrics['total_complaints'],
               name='Total Complaints', marker_color='#007bff'),
        row=1, col=1
    )
    
    # Avg resolution time
    fig.add_trace(
        go.Bar(x=dept_metrics['department'], y=dept_metrics['avg_resolution_time'],
               name='Avg Resolution Time', marker_color='#28a745'),
        row=1, col=2
    )
    
    # Avg satisfaction
    fig.add_trace(
        go.Bar(x=dept_metrics['department'], y=dept_metrics['avg_satisfaction'],
               name='Avg Satisfaction', marker_color='#ffc107'),
        row=2, col=1
    )
    
    # Scatter plot: complaints vs resolution time
    fig.add_trace(
        go.Scatter(x=dept_metrics['total_complaints'], y=dept_metrics['avg_resolution_time'],
                  mode='markers+text', name='Dept Performance',
                  text=dept_metrics['department'], textposition='top center',
                  marker=dict(size=10, color='#dc3545')),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Callbacks para Customer Analysis
@callback(
    [Output('total-customers', 'children'),
     Output('avg-monthly-bill', 'children'),
     Output('avg-satisfaction-score', 'children'),
     Output('high-churn-risk', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_customer_metrics(active_tab):
    if active_tab != "customer-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['customers']
    
    total_customers = len(df)
    avg_monthly_bill = f"${df['monthly_bill'].mean():.0f}"
    avg_satisfaction = f"{df['satisfaction_score'].mean():.1f}/10"
    high_churn_risk = len(df[df['churn_risk'] > 0.7])
    
    return total_customers, avg_monthly_bill, avg_satisfaction, high_churn_risk

@callback(
    Output('customer-demographics', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_customer_demographics(active_tab):
    if active_tab != "customer-tab":
        return go.Figure()
    
    try:
        df = data['customers'].copy()  # Hacer una copia para evitar modificar el original
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Age Distribution', 'Income Level Distribution', 
                           'Tenure Distribution', 'Regional Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Age Distribution
        age_bins = [18, 25, 35, 45, 55, 65, 80]
        age_labels = ['18-25', '26-35', '36-45', '46-55', '56-65', '65+']
        df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, include_lowest=True)
        age_dist = df['age_group'].value_counts()
        
        fig.add_trace(
            go.Bar(x=age_dist.index.astype(str), y=age_dist.values, name='Age Groups', marker_color='#007bff'),
            row=1, col=1
        )
        
        # Income Level Distribution
        income_dist = df['income_level'].value_counts()
        
        fig.add_trace(
            go.Bar(x=income_dist.index.astype(str), y=income_dist.values, name='Income Levels', marker_color='#28a745'),
            row=1, col=2
        )
        
        # Tenure Distribution
        tenure_bins = [0, 12, 24, 36, 48, 60, 120]
        tenure_labels = ['0-1y', '1-2y', '2-3y', '3-4y', '4-5y', '5y+']
        df['tenure_group'] = pd.cut(df['tenure_months'], bins=tenure_bins, labels=tenure_labels, include_lowest=True)
        tenure_dist = df['tenure_group'].value_counts()
        
        fig.add_trace(
            go.Bar(x=tenure_dist.index.astype(str), y=tenure_dist.values, name='Tenure Groups', marker_color='#ffc107'),
            row=2, col=1
        )
        
        # Regional Distribution
        region_dist = df['region'].value_counts()
        
        fig.add_trace(
            go.Bar(x=region_dist.index.astype(str), y=region_dist.values, name='Regions', marker_color='#dc3545'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        # En caso de error, devolver un gráfico vacío con mensaje de error
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Customer Demographics Analysis",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('customer-behavior', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_customer_behavior(active_tab):
    if active_tab != "customer-tab":
        return go.Figure()
    
    try:
        df = data['customers'].copy()  # Hacer una copia para evitar modificar el original
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Monthly Bill Distribution', 'Services Count Distribution', 
                           'Payment Method Distribution', 'Satisfaction Score Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Monthly Bill Distribution
        bill_bins = [0, 30, 50, 70, 90, 120]
        bill_labels = ['$0-30', '$30-50', '$50-70', '$70-90', '$90+']
        df['bill_group'] = pd.cut(df['monthly_bill'], bins=bill_bins, labels=bill_labels, include_lowest=True)
        bill_dist = df['bill_group'].value_counts()
        
        fig.add_trace(
            go.Bar(x=bill_dist.index.astype(str), y=bill_dist.values, name='Bill Groups', marker_color='#007bff'),
            row=1, col=1
        )
        
        # Services Count Distribution
        services_dist = df['services_count'].value_counts().sort_index()
        
        fig.add_trace(
            go.Bar(x=services_dist.index.astype(str), y=services_dist.values, name='Services Count', marker_color='#28a745'),
            row=1, col=2
        )
        
        # Payment Method Distribution
        payment_dist = df['payment_method'].value_counts()
        
        fig.add_trace(
            go.Bar(x=payment_dist.index.astype(str), y=payment_dist.values, name='Payment Methods', marker_color='#ffc107'),
            row=2, col=1
        )
        
        # Satisfaction Score Distribution
        satisfaction_dist = df['satisfaction_score'].value_counts().sort_index()
        
        fig.add_trace(
            go.Bar(x=satisfaction_dist.index.astype(str), y=satisfaction_dist.values, name='Satisfaction Scores', marker_color='#dc3545'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        # En caso de error, devolver un gráfico vacío con mensaje de error
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Customer Behavior Analysis",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('customer-segmentation', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_customer_segmentation(active_tab):
    if active_tab != "customer-tab":
        return go.Figure()
    
    df = data['customers']
    
    # Crear segmentos de clientes
    def segment_customers(row):
        if row['monthly_bill'] > 80 and row['satisfaction_score'] > 8:
            return 'High Value, Satisfied'
        elif row['monthly_bill'] > 80 and row['satisfaction_score'] <= 8:
            return 'High Value, At Risk'
        elif row['monthly_bill'] <= 80 and row['satisfaction_score'] > 8:
            return 'Low Value, Satisfied'
        else:
            return 'Low Value, At Risk'
    
    df['segment'] = df.apply(segment_customers, axis=1)
    segment_dist = df['segment'].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=segment_dist.index,
        values=segment_dist.values,
        hole=0.4,
        marker_colors=['#28a745', '#ffc107', '#007bff', '#dc3545'],
        textinfo='label+percent+value',
        textfont_size=12
    )])
    
    fig.update_layout(
        title="Customer Segmentation by Value and Satisfaction",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

@callback(
    Output('churn-risk-analysis', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_churn_risk_analysis(active_tab):
    if active_tab != "customer-tab":
        return go.Figure()
    
    df = data['customers']
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Churn Risk Distribution', 'Churn Risk vs Monthly Bill',
                       'Churn Risk vs Tenure', 'Churn Risk vs Satisfaction'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Churn Risk Distribution
    churn_bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    churn_labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
    df['churn_group'] = pd.cut(df['churn_risk'], bins=churn_bins, labels=churn_labels, include_lowest=True)
    churn_dist = df['churn_group'].value_counts()
    
    fig.add_trace(
        go.Bar(x=churn_dist.index, y=churn_dist.values, name='Churn Risk Groups', marker_color='#dc3545'),
        row=1, col=1
    )
    
    # Churn Risk vs Monthly Bill
    fig.add_trace(
        go.Scatter(x=df['monthly_bill'], y=df['churn_risk'], mode='markers',
                  name='Bill vs Churn', marker=dict(size=5, color='#007bff', opacity=0.6)),
        row=1, col=2
    )
    
    # Churn Risk vs Tenure
    fig.add_trace(
        go.Scatter(x=df['tenure_months'], y=df['churn_risk'], mode='markers',
                  name='Tenure vs Churn', marker=dict(size=5, color='#28a745', opacity=0.6)),
        row=2, col=1
    )
    
    # Churn Risk vs Satisfaction
    fig.add_trace(
        go.Scatter(x=df['satisfaction_score'], y=df['churn_risk'], mode='markers',
                  name='Satisfaction vs Churn', marker=dict(size=5, color='#ffc107', opacity=0.6)),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

# Callbacks para Network Analysis
@callback(
    [Output('avg-traffic-volume', 'children'),
     Output('avg-connection-speed', 'children'),
     Output('avg-uptime', 'children'),
     Output('avg-latency', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_network_metrics(active_tab):
    if active_tab != "network-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['network']
    
    avg_traffic = f"{df['traffic_volume_gbps'].mean():.1f} Gbps"
    avg_speed = f"{df['connection_speed_mbps'].mean():.0f} Mbps"
    avg_uptime = f"{df['uptime_percent'].mean():.2f}%"
    avg_latency = f"{df['latency_ms'].mean():.1f} ms"
    
    return avg_traffic, avg_speed, avg_uptime, avg_latency

@callback(
    Output('network-performance-trends', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_network_performance_trends(active_tab):
    if active_tab != "network-tab":
        return go.Figure()
    
    try:
        df = data['network'].copy()
        
        # Obtener datos de las últimas 24 horas
        last_24h = df.tail(24)
        
        fig = go.Figure()
        
        # Traffic Volume
        fig.add_trace(go.Scatter(
            x=last_24h['timestamp'],
            y=last_24h['traffic_volume_gbps'],
            mode='lines+markers',
            name='Traffic Volume (Gbps)',
            line=dict(color='#007bff', width=3),
            marker=dict(size=6),
            yaxis='y'
        ))
        
        # Connection Speed
        fig.add_trace(go.Scatter(
            x=last_24h['timestamp'],
            y=last_24h['connection_speed_mbps'],
            mode='lines+markers',
            name='Connection Speed (Mbps)',
            line=dict(color='#28a745', width=2),
            marker=dict(size=4),
            yaxis='y2'
        ))
        
        # Latency
        fig.add_trace(go.Scatter(
            x=last_24h['timestamp'],
            y=last_24h['latency_ms'],
            mode='lines+markers',
            name='Latency (ms)',
            line=dict(color='#ffc107', width=2),
            marker=dict(size=4),
            yaxis='y3'
        ))
        
        fig.update_layout(
            title="Network Performance Trends - Last 24 Hours",
            xaxis_title="Time",
            yaxis_title="Traffic Volume (Gbps)",
            yaxis2=dict(title="Connection Speed (Mbps)", overlaying='y', side='right'),
            yaxis3=dict(title="Latency (ms)", overlaying='y', side='right', position=0.95),
            height=400,
            showlegend=True,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Network Performance Trends",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('network-metrics-analysis', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_network_metrics_analysis(active_tab):
    if active_tab != "network-tab":
        return go.Figure()
    
    try:
        df = data['network'].copy()
        
        # Obtener datos de las últimas 24 horas
        last_24h = df.tail(24)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Active Connections', 'Packet Loss %', 'Bandwidth Utilization %', 'Uptime %'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Active Connections
        fig.add_trace(
            go.Bar(x=last_24h['timestamp'], y=last_24h['active_connections'],
                   name='Active Connections', marker_color='#007bff'),
            row=1, col=1
        )
        
        # Packet Loss
        fig.add_trace(
            go.Bar(x=last_24h['timestamp'], y=last_24h['packet_loss_percent'],
                   name='Packet Loss %', marker_color='#dc3545'),
            row=1, col=2
        )
        
        # Bandwidth Utilization
        fig.add_trace(
            go.Bar(x=last_24h['timestamp'], y=last_24h['bandwidth_utilization'],
                   name='Bandwidth Utilization %', marker_color='#28a745'),
            row=2, col=1
        )
        
        # Uptime
        fig.add_trace(
            go.Bar(x=last_24h['timestamp'], y=last_24h['uptime_percent'],
                   name='Uptime %', marker_color='#ffc107'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Network Metrics Analysis",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('bandwidth-utilization', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_bandwidth_utilization(active_tab):
    if active_tab != "network-tab":
        return go.Figure()
    
    try:
        df = data['network'].copy()
        
        # Categorizar utilización de ancho de banda
        def categorize_bandwidth(utilization):
            if utilization < 50:
                return 'Low (<50%)'
            elif utilization < 75:
                return 'Medium (50-75%)'
            elif utilization < 90:
                return 'High (75-90%)'
            else:
                return 'Critical (>90%)'
        
        df['bandwidth_category'] = df['bandwidth_utilization'].apply(categorize_bandwidth)
        bandwidth_dist = df['bandwidth_category'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=bandwidth_dist.index,
            values=bandwidth_dist.values,
            hole=0.4,
            marker_colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545'],
            textinfo='label+percent+value',
            textfont_size=12
        )])
        
        fig.update_layout(
            title="Bandwidth Utilization Distribution",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Bandwidth Utilization",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('network-health-dashboard', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_network_health_dashboard(active_tab):
    if active_tab != "network-tab":
        return go.Figure()
    
    try:
        df = data['network'].copy()
        
        # Obtener datos de las últimas 24 horas
        last_24h = df.tail(24)
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Network Health Score', 'Performance vs Time of Day',
                           'Latency vs Traffic Volume', 'Uptime vs Bandwidth Utilization'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Network Health Score (combinación de métricas)
        health_score = (last_24h['uptime_percent'] * 0.4 + 
                       (100 - last_24h['packet_loss_percent'] * 50) * 0.3 +
                       (100 - last_24h['latency_ms'] / 2) * 0.3)
        
        fig.add_trace(
            go.Scatter(x=last_24h['timestamp'], y=health_score,
                      mode='lines+markers', name='Health Score',
                      line=dict(color='#28a745', width=3)),
            row=1, col=1
        )
        
        # Performance vs Time of Day
        hour_performance = last_24h.groupby(last_24h['timestamp'].dt.hour)['traffic_volume_gbps'].mean()
        
        fig.add_trace(
            go.Bar(x=hour_performance.index, y=hour_performance.values,
                   name='Hourly Performance', marker_color='#007bff'),
            row=1, col=2
        )
        
        # Latency vs Traffic Volume
        fig.add_trace(
            go.Scatter(x=last_24h['traffic_volume_gbps'], y=last_24h['latency_ms'],
                      mode='markers', name='Latency vs Traffic',
                      marker=dict(size=8, color='#ffc107', opacity=0.6)),
            row=2, col=1
        )
        
        # Uptime vs Bandwidth Utilization
        fig.add_trace(
            go.Scatter(x=last_24h['bandwidth_utilization'], y=last_24h['uptime_percent'],
                      mode='markers', name='Uptime vs Bandwidth',
                      marker=dict(size=8, color='#dc3545', opacity=0.6)),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Network Health Dashboard",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

# Callbacks para Operations Analysis
@callback(
    [Output('total-invoices-processed', 'children'),
     Output('avg-processing-time', 'children'),
     Output('automation-rate', 'children'),
     Output('error-rate', 'children')],
    [Input('tabs', 'active_tab')]
)
def update_operations_metrics(active_tab):
    if active_tab != "operations-tab":
        return "N/A", "N/A", "N/A", "N/A"
    
    df = data['operations']
    
    total_invoices = f"{df['invoices_processed'].sum():,}"
    avg_processing = f"{df['processing_time_minutes'].mean():.1f} min"
    automation_rate = f"{df['automation_rate_percent'].mean():.1f}%"
    error_rate = f"{df['error_rate_percent'].mean():.2f}%"
    
    return total_invoices, avg_processing, automation_rate, error_rate

@callback(
    Output('operations-performance-trends', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_operations_performance_trends(active_tab):
    if active_tab != "operations-tab":
        return go.Figure()
    
    try:
        df = data['operations'].copy()
        
        fig = go.Figure()
        
        # Invoices Processed
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['invoices_processed'],
            mode='lines+markers',
            name='Invoices Processed',
            line=dict(color='#007bff', width=3),
            marker=dict(size=6),
            yaxis='y'
        ))
        
        # Processing Time
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['processing_time_minutes'],
            mode='lines+markers',
            name='Processing Time (min)',
            line=dict(color='#28a745', width=2),
            marker=dict(size=4),
            yaxis='y2'
        ))
        
        # Automation Rate
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['automation_rate_percent'],
            mode='lines+markers',
            name='Automation Rate (%)',
            line=dict(color='#ffc107', width=2),
            marker=dict(size=4),
            yaxis='y3'
        ))
        
        fig.update_layout(
            title="Operations Performance Trends - Last 30 Days",
            xaxis_title="Date",
            yaxis_title="Invoices Processed",
            yaxis2=dict(title="Processing Time (min)", overlaying='y', side='right'),
            yaxis3=dict(title="Automation Rate (%)", overlaying='y', side='right', position=0.95),
            height=400,
            showlegend=True,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Operations Performance Trends",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('operations-efficiency-analysis', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_operations_efficiency_analysis(active_tab):
    if active_tab != "operations-tab":
        return go.Figure()
    
    try:
        df = data['operations'].copy()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Staff Productivity', 'Error Rate %', 'Cost per Invoice', 'Customer Satisfaction'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Staff Productivity
        fig.add_trace(
            go.Bar(x=df['date'], y=df['staff_productivity'],
                   name='Staff Productivity', marker_color='#007bff'),
            row=1, col=1
        )
        
        # Error Rate
        fig.add_trace(
            go.Bar(x=df['date'], y=df['error_rate_percent'],
                   name='Error Rate %', marker_color='#dc3545'),
            row=1, col=2
        )
        
        # Cost per Invoice
        fig.add_trace(
            go.Bar(x=df['date'], y=df['cost_per_invoice'],
                   name='Cost per Invoice ($)', marker_color='#28a745'),
            row=2, col=1
        )
        
        # Customer Satisfaction
        fig.add_trace(
            go.Bar(x=df['date'], y=df['customer_satisfaction'],
                   name='Customer Satisfaction', marker_color='#ffc107'),
            row=2, col=2
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Operations Efficiency Analysis",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('cost-analysis', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_cost_analysis(active_tab):
    if active_tab != "operations-tab":
        return go.Figure()
    
    try:
        df = data['operations'].copy()
        
        # Categorizar costos por operación
        def categorize_cost(cost):
            if cost < 1.5:
                return 'Low Cost (<$1.50)'
            elif cost < 2.5:
                return 'Medium Cost ($1.50-$2.50)'
            elif cost < 3.5:
                return 'High Cost ($2.50-$3.50)'
            else:
                return 'Very High Cost (>$3.50)'
        
        df['cost_category'] = df['cost_per_invoice'].apply(categorize_cost)
        cost_dist = df['cost_category'].value_counts()
        
        fig = go.Figure(data=[go.Pie(
            labels=cost_dist.index,
            values=cost_dist.values,
            hole=0.4,
            marker_colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545'],
            textinfo='label+percent+value',
            textfont_size=12
        )])
        
        fig.update_layout(
            title="Cost Analysis by Operation",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Cost Analysis",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

@callback(
    Output('operations-health-dashboard', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_operations_health_dashboard(active_tab):
    if active_tab != "operations-tab":
        return go.Figure()
    
    try:
        df = data['operations'].copy()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Operations Health Score', 'Efficiency vs Cost',
                           'Productivity vs Satisfaction', 'Automation vs Error Rate'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Operations Health Score (combinación de métricas)
        health_score = (df['staff_productivity'] * 0.3 + 
                       (10 - df['error_rate_percent']) * 0.2 +
                       df['customer_satisfaction'] * 0.3 +
                       df['automation_rate_percent'] / 10 * 0.2)
        
        fig.add_trace(
            go.Scatter(x=df['date'], y=health_score,
                      mode='lines+markers', name='Health Score',
                      line=dict(color='#28a745', width=3)),
            row=1, col=1
        )
        
        # Efficiency vs Cost
        fig.add_trace(
            go.Scatter(x=df['cost_per_invoice'], y=df['staff_productivity'],
                      mode='markers', name='Efficiency vs Cost',
                      marker=dict(size=8, color='#007bff', opacity=0.6)),
            row=1, col=2
        )
        
        # Productivity vs Satisfaction
        fig.add_trace(
            go.Scatter(x=df['staff_productivity'], y=df['customer_satisfaction'],
                      mode='markers', name='Productivity vs Satisfaction',
                      marker=dict(size=8, color='#ffc107', opacity=0.6)),
            row=2, col=1
        )
        
        # Automation vs Error Rate
        fig.add_trace(
            go.Scatter(x=df['automation_rate_percent'], y=df['error_rate_percent'],
                      mode='markers', name='Automation vs Error Rate',
                      marker=dict(size=8, color='#dc3545', opacity=0.6)),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading data: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="red")
        )
        fig.update_layout(
            title="Operations Health Dashboard",
            height=400,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        return fig

# =============================================================================
# 6. CONFIGURACIÓN DEL SERVIDOR
# =============================================================================
server = app.server

if __name__ == '__main__':
    app.run_server(
        debug=True,
        host='127.0.0.1',
        port=8051
    )
