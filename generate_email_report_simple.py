import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Generar datos sintéticos
def generate_synthetic_data():
    np.random.seed(42)
    
    # Real-time data
    timestamps = pd.date_range(start=datetime.now() - timedelta(hours=23), 
                              end=datetime.now(), freq='H')
    
    real_time_data = []
    for ts in timestamps:
        real_time_data.append({
            'timestamp': ts,
            'total_revenue': np.random.uniform(50000, 150000),
            'voice_revenue': np.random.uniform(20000, 60000),
            'data_revenue': np.random.uniform(30000, 90000),
            'calls_volume': np.random.randint(1000, 5000),
            'data_volume_gb': np.random.uniform(500, 2000),
            'messages_volume': np.random.randint(5000, 15000)
        })
    
    real_time = pd.DataFrame(real_time_data)
    
    # VIP Customers
    vip_data = []
    for i in range(50):
        for day in range(30):
            vip_data.append({
                'customer_id': f'VIP_{i+1:03d}',
                'date': datetime.now() - timedelta(days=29-day),
                'voice_usage_minutes': np.random.uniform(200, 800),
                'data_usage_gb': np.random.uniform(50, 200),
                'monthly_bill': np.random.uniform(150, 500),
                'satisfaction_score': np.random.uniform(7, 10),
                'service_level': np.random.choice(['Premium', 'Enterprise', 'Gold']),
                'pending_amount': np.random.uniform(0, 100)
            })
    
    vip_customers = pd.DataFrame(vip_data)
    
    # Departments
    departments = ['Sales', 'Marketing', 'Engineering', 'Finance', 'HR', 'Operations', 'Support']
    dept_data = []
    for dept in departments:
        for day in range(30):
            dept_data.append({
                'department': dept,
                'date': datetime.now() - timedelta(days=29-day),
                'billed_amount': np.random.uniform(10000, 100000),
                'active_users': np.random.randint(50, 300),
                'efficiency_score': np.random.uniform(0.7, 0.95),
                'cost_per_user': np.random.uniform(50, 200)
            })
    
    departments_df = pd.DataFrame(dept_data)
    
    # Products
    products = ['Internet Basic', 'Internet Premium', 'Cable TV', 'Phone Service', 'Bundle Package']
    product_data = []
    for product in products:
        for day in range(30):
            product_data.append({
                'product': product,
                'date': datetime.now() - timedelta(days=29-day),
                'billed_amount': np.random.uniform(5000, 50000),
                'subscribers': np.random.randint(100, 1000),
                'churn_rate': np.random.uniform(0.02, 0.08),
                'profit_margin': np.random.uniform(0.15, 0.35)
            })
    
    products_df = pd.DataFrame(product_data)
    
    # Complaints
    complaint_types = ['Billing Issue', 'Service Outage', 'Speed Problem', 'Customer Service']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    depts = ['Support', 'Billing', 'Technical', 'Sales']
    
    complaints_data = []
    for day in range(30):
        daily_complaints = np.random.randint(10, 50)
        for _ in range(daily_complaints):
            complaints_data.append({
                'date': datetime.now() - timedelta(days=29-day),
                'complaint_type': np.random.choice(complaint_types),
                'priority': np.random.choice(priorities),
                'resolution_time_hours': np.random.uniform(1, 72),
                'satisfaction_score': np.random.uniform(1, 10),
                'department': np.random.choice(depts),
                'resolved': np.random.choice([True, False], p=[0.85, 0.15])
            })
    
    complaints = pd.DataFrame(complaints_data)
    
    # Customers
    customer_data = []
    for i in range(1000):
        customer_data.append({
            'customer_id': f'CUST_{i+1:04d}',
            'age': np.random.randint(18, 80),
            'income_level': np.random.choice(['Low', 'Medium', 'High', 'Very High']),
            'tenure_months': np.random.randint(1, 120),
            'region': np.random.choice(['North', 'South', 'East', 'West', 'Central']),
            'monthly_bill': np.random.uniform(50, 300),
            'services_count': np.random.randint(1, 5),
            'payment_method': np.random.choice(['Credit Card', 'Bank Transfer', 'Cash', 'Digital Wallet']),
            'satisfaction_score': np.random.uniform(1, 10),
            'churn_risk': np.random.uniform(0, 1)
        })
    
    customers = pd.DataFrame(customer_data)
    
    # Network
    network_data = []
    for hour in range(24):
        network_data.append({
            'timestamp': datetime.now() - timedelta(hours=23-hour),
            'traffic_volume_gbps': np.random.uniform(50, 200),
            'connection_speed_mbps': np.random.uniform(100, 1000),
            'uptime_percentage': np.random.uniform(95, 99.9),
            'latency_ms': np.random.uniform(5, 50),
            'active_connections': np.random.randint(10000, 50000),
            'packet_loss_percentage': np.random.uniform(0, 2),
            'bandwidth_utilization': np.random.uniform(30, 90)
        })
    
    network = pd.DataFrame(network_data)
    
    # Operations
    operations_data = []
    for day in range(30):
        operations_data.append({
            'date': datetime.now() - timedelta(days=29-day),
            'invoices_processed': np.random.randint(500, 2000),
            'processing_time_minutes': np.random.uniform(5, 30),
            'automation_rate': np.random.uniform(0.6, 0.95),
            'error_rate': np.random.uniform(0.01, 0.05),
            'staff_productivity': np.random.uniform(0.7, 0.95),
            'cost_per_invoice': np.random.uniform(2, 10),
            'customer_satisfaction': np.random.uniform(7, 10)
        })
    
    operations = pd.DataFrame(operations_data)
    
    return {
        'real_time': real_time,
        'vip_customers': vip_customers,
        'departments': departments_df,
        'products': products_df,
        'complaints': complaints,
        'customers': customers,
        'network': network,
        'operations': operations
    }

# Generar gráficos principales
def generate_main_charts():
    data = generate_synthetic_data()
    charts = {}
    
    # 1. Revenue Trends
    df = data['real_time']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['total_revenue'], 
                            mode='lines+markers', name='Total Revenue', line=dict(color='#007bff', width=3)))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['voice_revenue'], 
                            mode='lines+markers', name='Voice Revenue', line=dict(color='#28a745', width=2)))
    fig.update_layout(title="Revenue Trends - Last 24 Hours", height=400)
    charts['revenue_trends'] = fig.to_json()
    
    # 2. VIP Performance
    df = data['vip_customers']
    latest_vip = df.groupby('customer_id').last().reset_index()
    top_10 = latest_vip.nlargest(10, 'monthly_bill')
    fig = go.Figure(data=[go.Bar(x=top_10['customer_id'], y=top_10['monthly_bill'], 
                                marker_color='#007bff')])
    fig.update_layout(title="Top 10 VIP Customers by Monthly Bill", height=400)
    charts['vip_performance'] = fig.to_json()
    
    # 3. Department Performance
    df = data['departments']
    latest_dept = df.groupby('department').last().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_dept['department'], y=latest_dept['billed_amount'], 
                        name='Billed Amount', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=latest_dept['department'], y=latest_dept['active_users'], 
                        name='Active Users', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Department Performance", yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['dept_performance'] = fig.to_json()
    
    # 4. Product Performance
    df = data['products']
    latest_products = df.groupby('product').last().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['billed_amount'], 
                        name='Revenue', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['subscribers'], 
                        name='Subscribers', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Product Performance", yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['product_performance'] = fig.to_json()
    
    # 5. Complaints Timeline
    df = data['complaints']
    daily_complaints = df.groupby('date').size().reset_index(name='count')
    fig = go.Figure(data=[go.Scatter(x=daily_complaints['date'], y=daily_complaints['count'], 
                                    mode='lines+markers', line=dict(color='#dc3545'))])
    fig.update_layout(title="Complaints Timeline", height=400)
    charts['complaints_timeline'] = fig.to_json()
    
    # 6. Customer Demographics
    df = data['customers']
    fig = go.Figure(data=[go.Histogram(x=df['age'], nbinsx=20, marker_color='#007bff')])
    fig.update_layout(title="Customer Age Distribution", height=400)
    charts['customer_demographics'] = fig.to_json()
    
    # 7. Network Performance
    df = data['network']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['traffic_volume_gbps'], 
                            mode='lines+markers', name='Traffic Volume', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['connection_speed_mbps'], 
                            mode='lines+markers', name='Connection Speed', line=dict(color='#28a745'), yaxis='y2'))
    fig.update_layout(title="Network Performance", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['network_performance'] = fig.to_json()
    
    # 8. Operations Performance
    df = data['operations']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['invoices_processed'], 
                            mode='lines+markers', name='Invoices Processed', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=df['date'], y=df['automation_rate']*100, 
                            mode='lines+markers', name='Automation Rate (%)', line=dict(color='#28a745'), yaxis='y2'))
    fig.update_layout(title="Operations Performance", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['operations_performance'] = fig.to_json()
    
    return charts, data

# Generar HTML
def generate_html_report():
    charts, data = generate_main_charts()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Charter Spectrum - Billing Operations Dashboard Report</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f8f9fa;
            }}
            .header {{
                background: linear-gradient(135deg, #007bff, #0056b3);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 10px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .section {{
                background: white;
                margin: 20px 0;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .section h2 {{
                color: #007bff;
                border-bottom: 2px solid #007bff;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            .metric {{
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                border-left: 4px solid #007bff;
            }}
            .metric h3 {{
                margin: 0;
                color: #007bff;
                font-size: 24px;
            }}
            .metric p {{
                margin: 5px 0 0 0;
                color: #6c757d;
                font-size: 14px;
            }}
            .chart-container {{
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                color: #6c757d;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Charter Spectrum - Billing Operations Dashboard</h1>
            <p>Comprehensive Report - {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <div class="section">
            <h2>📈 Real-time Billing Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>${data['real_time']['total_revenue'].sum():,.0f}</h3>
                    <p>Total Revenue (24h)</p>
                </div>
                <div class="metric">
                    <h3>{data['real_time']['calls_volume'].sum():,}</h3>
                    <p>Calls Volume</p>
                </div>
                <div class="metric">
                    <h3>{data['real_time']['data_volume_gb'].sum():,.0f}</h3>
                    <p>Data Volume (GB)</p>
                </div>
                <div class="metric">
                    <h3>{data['real_time']['messages_volume'].sum():,}</h3>
                    <p>Messages Volume</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="revenue-trends"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>👑 VIP Customers Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>{len(data['vip_customers']['customer_id'].unique())}</h3>
                    <p>Total VIP Customers</p>
                </div>
                <div class="metric">
                    <h3>${data['vip_customers']['monthly_bill'].mean():.0f}</h3>
                    <p>Avg VIP Bill</p>
                </div>
                <div class="metric">
                    <h3>{data['vip_customers']['satisfaction_score'].mean():.1f}</h3>
                    <p>VIP Satisfaction</p>
                </div>
                <div class="metric">
                    <h3>${data['vip_customers']['pending_amount'].sum():,.0f}</h3>
                    <p>Pending VIP Amount</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="vip-performance"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>🏢 Department Billing Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>${data['departments']['billed_amount'].sum():,.0f}</h3>
                    <p>Total Billed by Depts</p>
                </div>
                <div class="metric">
                    <h3>{data['departments']['efficiency_score'].mean():.1%}</h3>
                    <p>Avg Dept Efficiency</p>
                </div>
                <div class="metric">
                    <h3>{data['departments']['active_users'].sum():,}</h3>
                    <p>Total Active Users</p>
                </div>
                <div class="metric">
                    <h3>${data['departments']['cost_per_user'].mean():.0f}</h3>
                    <p>Avg Cost per User</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="dept-performance"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>📦 Product Billing Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>${data['products']['billed_amount'].sum():,.0f}</h3>
                    <p>Total Product Revenue</p>
                </div>
                <div class="metric">
                    <h3>{data['products']['subscribers'].sum():,}</h3>
                    <p>Total Subscribers</p>
                </div>
                <div class="metric">
                    <h3>{data['products']['churn_rate'].mean():.1%}</h3>
                    <p>Avg Churn Rate</p>
                </div>
                <div class="metric">
                    <h3>{data['products']['profit_margin'].mean():.1%}</h3>
                    <p>Avg Profit Margin</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="product-performance"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>⚠️ Complaints & Resolutions Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>{len(data['complaints'])}</h3>
                    <p>Total Complaints</p>
                </div>
                <div class="metric">
                    <h3>{data['complaints']['resolution_time_hours'].mean():.1f}h</h3>
                    <p>Avg Resolution Time</p>
                </div>
                <div class="metric">
                    <h3>{data['complaints']['satisfaction_score'].mean():.1f}</h3>
                    <p>Avg Satisfaction</p>
                </div>
                <div class="metric">
                    <h3>{data['complaints']['resolved'].mean():.1%}</h3>
                    <p>Resolution Rate</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="complaints-timeline"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>👥 Customer Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>{len(data['customers'])}</h3>
                    <p>Total Customers</p>
                </div>
                <div class="metric">
                    <h3>${data['customers']['monthly_bill'].mean():.0f}</h3>
                    <p>Avg Monthly Bill</p>
                </div>
                <div class="metric">
                    <h3>{data['customers']['satisfaction_score'].mean():.1f}</h3>
                    <p>Avg Satisfaction</p>
                </div>
                <div class="metric">
                    <h3>{len(data['customers'][data['customers']['churn_risk'] > 0.7])}</h3>
                    <p>High Churn Risk</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="customer-demographics"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>🌐 Network Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>{data['network']['traffic_volume_gbps'].mean():.1f}</h3>
                    <p>Avg Traffic Volume (Gbps)</p>
                </div>
                <div class="metric">
                    <h3>{data['network']['connection_speed_mbps'].mean():.0f}</h3>
                    <p>Avg Connection Speed (Mbps)</p>
                </div>
                <div class="metric">
                    <h3>{data['network']['uptime_percentage'].mean():.1f}%</h3>
                    <p>Avg Uptime</p>
                </div>
                <div class="metric">
                    <h3>{data['network']['latency_ms'].mean():.1f}ms</h3>
                    <p>Avg Latency</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="network-performance"></div>
            </div>
        </div>
        
        <div class="section">
            <h2>⚙️ Operations Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>{data['operations']['invoices_processed'].sum():,}</h3>
                    <p>Total Invoices Processed</p>
                </div>
                <div class="metric">
                    <h3>{data['operations']['processing_time_minutes'].mean():.1f}min</h3>
                    <p>Avg Processing Time</p>
                </div>
                <div class="metric">
                    <h3>{data['operations']['automation_rate'].mean():.1%}</h3>
                    <p>Automation Rate</p>
                </div>
                <div class="metric">
                    <h3>{data['operations']['error_rate'].mean():.1%}</h3>
                    <p>Error Rate</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="operations-performance"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>📊 This report was generated automatically on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>All data is synthetic and for demonstration purposes</p>
        </div>
        
        <script>
            // Render all charts
            Plotly.newPlot('revenue-trends', {charts['revenue_trends']});
            Plotly.newPlot('vip-performance', {charts['vip_performance']});
            Plotly.newPlot('dept-performance', {charts['dept_performance']});
            Plotly.newPlot('product-performance', {charts['product_performance']});
            Plotly.newPlot('complaints-timeline', {charts['complaints_timeline']});
            Plotly.newPlot('customer-demographics', {charts['customer_demographics']});
            Plotly.newPlot('network-performance', {charts['network_performance']});
            Plotly.newPlot('operations-performance', {charts['operations_performance']});
        </script>
    </body>
    </html>
    """
    
    # Guardar el archivo HTML
    with open('billing_dashboard_report_simple.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Reporte HTML simplificado generado exitosamente: billing_dashboard_report_simple.html")
    print("📧 Este archivo se puede enviar por email o abrir en cualquier navegador")
    
    return html_content

if __name__ == "__main__":
    generate_html_report()
