import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Exact same data generation function as billing_dashboard.py
def generate_synthetic_data():
    np.random.seed(42)
    random.seed(42)
    
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='H')
    
    # Real-time data
    real_time_data = []
    for date in dates:
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
    
    # VIP Customers
    vip_customers = []
    customer_ids = [f'VIP_{i:03d}' for i in range(1, 21)]
    for customer_id in customer_ids:
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
    
    # Departments
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
    
    # Products
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
    
    # Complaints
    complaint_types = ['Billing Error', 'Service Outage', 'Speed Issues', 'Customer Service', 
                      'Installation Problem', 'Equipment Issue', 'Contract Dispute']
    resolution_times = [1, 2, 3, 5, 7, 10, 15]
    
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
    
    # Customers
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
    
    # Network
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
    
    # Operations
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

# Generate all charts using the exact same logic as billing_dashboard.py
def generate_all_charts():
    data = generate_synthetic_data()
    charts = {}
    
    # 1. Real-time Revenue Trends
    df = data['real_time'].tail(24)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['total_revenue'], 
                            mode='lines+markers', name='Total Revenue', 
                            line=dict(color='#007bff', width=3), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['voice_revenue'], 
                            mode='lines+markers', name='Voice Revenue', 
                            line=dict(color='#28a745', width=2), marker=dict(size=4)))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['data_revenue'], 
                            mode='lines+markers', name='Data Revenue', 
                            line=dict(color='#ffc107', width=2), marker=dict(size=4)))
    fig.update_layout(title="Revenue Trends - Last 24 Hours", height=400)
    charts['revenue_trends'] = fig.to_json()
    
    # 2. Service Usage Subplots
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Calls Volume', 'Messages Volume', 'Data Volume', 'Revenue per Hour'))
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['calls_volume'], name='Calls', marker_color='#007bff'), row=1, col=1)
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['messages_volume'], name='Messages', marker_color='#28a745'), row=1, col=2)
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['data_volume_gb'], name='Data (GB)', marker_color='#ffc107'), row=2, col=1)
    fig.add_trace(go.Bar(x=df['timestamp'], y=df['total_revenue'], name='Revenue ($)', marker_color='#dc3545'), row=2, col=2)
    fig.update_layout(height=500, showlegend=False)
    charts['service_usage'] = fig.to_json()
    
    # 3. Revenue Distribution Pie
    voice_total = df['voice_revenue'].sum()
    data_total = df['data_revenue'].sum()
    fig = go.Figure(data=[go.Pie(labels=['Voice Revenue', 'Data Revenue'], 
                                values=[voice_total, data_total], hole=0.4)])
    fig.update_layout(title="Revenue Distribution", height=400)
    charts['revenue_distribution'] = fig.to_json()
    
    # 4. VIP Usage Trends
    vip_df = data['vip_customers']
    latest_vip = vip_df.groupby('customer_id').last().reset_index()
    top_10 = latest_vip.nlargest(10, 'monthly_bill')
    fig = go.Figure(data=[go.Bar(x=top_10['customer_id'], y=top_10['monthly_bill'], marker_color='#007bff')])
    fig.update_layout(title="Top 10 VIP Customers by Monthly Bill", height=400)
    charts['vip_usage_trends'] = fig.to_json()
    
    # 5. VIP Performance
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vip_df['date'], y=vip_df['voice_usage_minutes'], 
                            mode='lines', name='Voice Usage', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=vip_df['date'], y=vip_df['data_usage_gb'], 
                            mode='lines', name='Data Usage', line=dict(color='#28a745'), yaxis='y2'))
    fig.update_layout(title="VIP Customer Performance Trends", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['vip_performance'] = fig.to_json()
    
    # 6. VIP Service Level Distribution
    service_counts = vip_df['service_level'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=service_counts.index, values=service_counts.values)])
    fig.update_layout(title="VIP Service Level Distribution", height=400)
    charts['vip_service_levels'] = fig.to_json()
    
    # 7. Department Billing Trends
    dept_df = data['departments']
    latest_dept = dept_df.groupby('department').last().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_dept['department'], y=latest_dept['billed_amount'], 
                        name='Billed Amount', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=latest_dept['department'], y=latest_dept['active_users'], 
                        name='Active Users', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Department Performance", yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['dept_billing_trends'] = fig.to_json()
    
    # 8. Department Performance
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dept_df['date'], y=dept_df['efficiency_score'], 
                            mode='lines+markers', name='Efficiency Score', line=dict(color='#007bff')))
    fig.update_layout(title="Department Efficiency Trends", height=400)
    charts['dept_performance'] = fig.to_json()
    
    # 9. Department Efficiency
    fig = go.Figure(data=[go.Bar(x=latest_dept['department'], y=latest_dept['efficiency_score'], marker_color='#28a745')])
    fig.update_layout(title="Department Efficiency Scores", height=400)
    charts['dept_efficiency'] = fig.to_json()
    
    # 10. Product Revenue Trends
    product_df = data['products']
    latest_products = product_df.groupby('product').last().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['billed_amount'], 
                        name='Revenue', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['subscribers'], 
                        name='Subscribers', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Product Performance", yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['product_revenue_trends'] = fig.to_json()
    
    # 11. Product Performance
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=product_df['date'], y=product_df['revenue_per_subscriber'], 
                            mode='lines+markers', name='Revenue per Subscriber', line=dict(color='#007bff')))
    fig.update_layout(title="Product Revenue per Subscriber Trends", height=400)
    charts['product_performance'] = fig.to_json()
    
    # 12. Product Revenue Distribution
    fig = go.Figure(data=[go.Pie(labels=latest_products['product'], values=latest_products['billed_amount'])])
    fig.update_layout(title="Product Revenue Distribution", height=400)
    charts['product_revenue_distribution'] = fig.to_json()
    
    # 13. Product Churn Analysis
    fig = go.Figure(data=[go.Bar(x=latest_products['product'], y=latest_products['churn_rate'], marker_color='#dc3545')])
    fig.update_layout(title="Product Churn Rates", height=400)
    charts['product_churn_analysis'] = fig.to_json()
    
    # 14. Complaints Timeline
    complaints_df = data['complaints']
    daily_complaints = complaints_df.groupby('complaint_date').size().reset_index(name='count')
    fig = go.Figure(data=[go.Scatter(x=daily_complaints['complaint_date'], y=daily_complaints['count'], 
                                    mode='lines+markers', line=dict(color='#dc3545'))])
    fig.update_layout(title="Complaints Timeline", height=400)
    charts['complaints_timeline'] = fig.to_json()
    
    # 15. Complaints by Type
    complaint_counts = complaints_df['complaint_type'].value_counts()
    fig = go.Figure(data=[go.Bar(x=complaint_counts.index, y=complaint_counts.values, marker_color='#dc3545')])
    fig.update_layout(title="Complaints by Type", height=400)
    charts['complaints_by_type'] = fig.to_json()
    
    # 16. Resolution Time Distribution
    fig = go.Figure(data=[go.Histogram(x=complaints_df['resolution_time_days'], nbinsx=10, marker_color='#007bff')])
    fig.update_layout(title="Resolution Time Distribution", height=400)
    charts['resolution_time_distribution'] = fig.to_json()
    
    # 17. Department Complaints Performance
    dept_complaints = complaints_df.groupby('department').agg({
        'complaint_id': 'count',
        'resolution_time_days': 'mean',
        'customer_satisfaction': 'mean'
    }).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dept_complaints['department'], y=dept_complaints['complaint_id'], 
                        name='Complaints Count', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=dept_complaints['department'], y=dept_complaints['resolution_time_days'], 
                        name='Avg Resolution Time', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Department Complaints Performance", yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['dept_complaints_performance'] = fig.to_json()
    
    # 18. Customer Demographics
    customer_df = data['customers']
    fig = go.Figure(data=[go.Histogram(x=customer_df['age'], nbinsx=20, marker_color='#007bff')])
    fig.update_layout(title="Customer Age Distribution", height=400)
    charts['customer_demographics'] = fig.to_json()
    
    # 19. Customer Behavior
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=customer_df['tenure_months'], y=customer_df['monthly_bill'], 
                            mode='markers', marker=dict(color=customer_df['satisfaction_score'], 
                            colorscale='Viridis', size=8)))
    fig.update_layout(title="Customer Behavior Analysis", height=400)
    charts['customer_behavior'] = fig.to_json()
    
    # 20. Customer Segmentation
    income_counts = customer_df['income_level'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=income_counts.index, values=income_counts.values)])
    fig.update_layout(title="Customer Income Level Distribution", height=400)
    charts['customer_segmentation'] = fig.to_json()
    
    # 21. Churn Risk Analysis
    fig = go.Figure(data=[go.Histogram(x=customer_df['churn_risk'], nbinsx=20, marker_color='#dc3545')])
    fig.update_layout(title="Customer Churn Risk Distribution", height=400)
    charts['churn_risk_analysis'] = fig.to_json()
    
    # 22. Network Performance Trends
    network_df = data['network']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=network_df['timestamp'], y=network_df['traffic_volume_gbps'], 
                            mode='lines+markers', name='Traffic Volume', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=network_df['timestamp'], y=network_df['connection_speed_mbps'], 
                            mode='lines+markers', name='Connection Speed', line=dict(color='#28a745'), yaxis='y2'))
    fig.update_layout(title="Network Performance Trends", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['network_performance_trends'] = fig.to_json()
    
    # 23. Network Metrics Analysis
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=network_df['timestamp'], y=network_df['latency_ms'], 
                            mode='lines+markers', name='Latency', line=dict(color='#dc3545')))
    fig.add_trace(go.Scatter(x=network_df['timestamp'], y=network_df['uptime_percent'], 
                            mode='lines+markers', name='Uptime %', line=dict(color='#28a745'), yaxis='y2'))
    fig.update_layout(title="Network Health Metrics", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['network_metrics_analysis'] = fig.to_json()
    
    # 24. Bandwidth Utilization
    fig = go.Figure(data=[go.Scatter(x=network_df['timestamp'], y=network_df['bandwidth_utilization'], 
                                    mode='lines+markers', line=dict(color='#007bff'))])
    fig.update_layout(title="Bandwidth Utilization", height=400)
    charts['bandwidth_utilization'] = fig.to_json()
    
    # 25. Network Health Dashboard
    latest_network = network_df.tail(1).iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Indicator(mode="gauge+number", value=latest_network['uptime_percent'], 
                              title={'text': "Uptime %"}, gauge={'axis': {'range': [None, 100]}}))
    fig.update_layout(title="Network Health Dashboard", height=400)
    charts['network_health_dashboard'] = fig.to_json()
    
    # 26. Operations Performance Trends
    operations_df = data['operations']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=operations_df['date'], y=operations_df['invoices_processed'], 
                            mode='lines+markers', name='Invoices Processed', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=operations_df['date'], y=operations_df['automation_rate_percent'], 
                            mode='lines+markers', name='Automation Rate %', line=dict(color='#28a745'), yaxis='y2'))
    fig.update_layout(title="Operations Performance Trends", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['operations_performance_trends'] = fig.to_json()
    
    # 27. Operations Efficiency Analysis
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=operations_df['date'], y=operations_df['staff_productivity'], 
                            mode='lines+markers', name='Staff Productivity', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=operations_df['date'], y=operations_df['error_rate_percent'], 
                            mode='lines+markers', name='Error Rate %', line=dict(color='#dc3545'), yaxis='y2'))
    fig.update_layout(title="Operations Efficiency Analysis", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['operations_efficiency_analysis'] = fig.to_json()
    
    # 28. Cost Analysis
    fig = go.Figure(data=[go.Scatter(x=operations_df['date'], y=operations_df['cost_per_invoice'], 
                                    mode='lines+markers', line=dict(color='#007bff'))])
    fig.update_layout(title="Cost per Invoice Trends", height=400)
    charts['cost_analysis'] = fig.to_json()
    
    # 29. Operations Health Dashboard
    latest_ops = operations_df.tail(1).iloc[0]
    fig = go.Figure()
    fig.add_trace(go.Indicator(mode="gauge+number", value=latest_ops['automation_rate_percent'], 
                              title={'text': "Automation Rate %"}, gauge={'axis': {'range': [None, 100]}}))
    fig.update_layout(title="Operations Health Dashboard", height=400)
    charts['operations_health_dashboard'] = fig.to_json()
    
    return charts, data

def generate_html_report():
    charts, data = generate_all_charts()
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Charter Spectrum - Complete Billing Operations Dashboard Report</title>
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
            <h1>📊 Charter Spectrum - Complete Billing Operations Dashboard</h1>
            <p>Comprehensive Report with All Charts - {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <div class="section">
            <h2>📈 Real-time Billing Analysis</h2>
            <div class="metrics">
                <div class="metric">
                    <h3>${data['real_time'].tail(24)['total_revenue'].sum():,.0f}</h3>
                    <p>Total Revenue (24h)</p>
                </div>
                <div class="metric">
                    <h3>{data['real_time'].tail(24)['calls_volume'].sum():,}</h3>
                    <p>Calls Volume</p>
                </div>
                <div class="metric">
                    <h3>{data['real_time'].tail(24)['data_volume_gb'].sum():,.0f}</h3>
                    <p>Data Volume (GB)</p>
                </div>
                <div class="metric">
                    <h3>{data['real_time'].tail(24)['messages_volume'].sum():,}</h3>
                    <p>Messages Volume</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="revenue-trends"></div>
            </div>
            <div class="chart-container">
                <div id="service-usage"></div>
            </div>
            <div class="chart-container">
                <div id="revenue-distribution"></div>
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
                <div id="vip-usage-trends"></div>
            </div>
            <div class="chart-container">
                <div id="vip-performance"></div>
            </div>
            <div class="chart-container">
                <div id="vip-service-levels"></div>
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
                <div id="dept-billing-trends"></div>
            </div>
            <div class="chart-container">
                <div id="dept-performance"></div>
            </div>
            <div class="chart-container">
                <div id="dept-efficiency"></div>
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
                <div id="product-revenue-trends"></div>
            </div>
            <div class="chart-container">
                <div id="product-performance"></div>
            </div>
            <div class="chart-container">
                <div id="product-revenue-distribution"></div>
            </div>
            <div class="chart-container">
                <div id="product-churn-analysis"></div>
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
                    <h3>{data['complaints']['resolution_time_days'].mean():.1f}d</h3>
                    <p>Avg Resolution Time</p>
                </div>
                <div class="metric">
                    <h3>{data['complaints']['customer_satisfaction'].mean():.1f}</h3>
                    <p>Avg Satisfaction</p>
                </div>
                <div class="metric">
                    <h3>{(data['complaints']['status'] == 'Resolved').mean():.1%}</h3>
                    <p>Resolution Rate</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="complaints-timeline"></div>
            </div>
            <div class="chart-container">
                <div id="complaints-by-type"></div>
            </div>
            <div class="chart-container">
                <div id="resolution-time-distribution"></div>
            </div>
            <div class="chart-container">
                <div id="dept-complaints-performance"></div>
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
            <div class="chart-container">
                <div id="customer-behavior"></div>
            </div>
            <div class="chart-container">
                <div id="customer-segmentation"></div>
            </div>
            <div class="chart-container">
                <div id="churn-risk-analysis"></div>
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
                    <h3>{data['network']['uptime_percent'].mean():.1f}%</h3>
                    <p>Avg Uptime</p>
                </div>
                <div class="metric">
                    <h3>{data['network']['latency_ms'].mean():.1f}ms</h3>
                    <p>Avg Latency</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="network-performance-trends"></div>
            </div>
            <div class="chart-container">
                <div id="network-metrics-analysis"></div>
            </div>
            <div class="chart-container">
                <div id="bandwidth-utilization"></div>
            </div>
            <div class="chart-container">
                <div id="network-health-dashboard"></div>
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
                    <h3>{data['operations']['automation_rate_percent'].mean():.1f}%</h3>
                    <p>Automation Rate</p>
                </div>
                <div class="metric">
                    <h3>{data['operations']['error_rate_percent'].mean():.1f}%</h3>
                    <p>Error Rate</p>
                </div>
            </div>
            <div class="chart-container">
                <div id="operations-performance-trends"></div>
            </div>
            <div class="chart-container">
                <div id="operations-efficiency-analysis"></div>
            </div>
            <div class="chart-container">
                <div id="cost-analysis"></div>
            </div>
            <div class="chart-container">
                <div id="operations-health-dashboard"></div>
            </div>
        </div>
        
        <div class="footer">
            <p>📊 This complete report was generated automatically on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>All data is synthetic and for demonstration purposes</p>
        </div>
        
        <script>
            // Render all charts using the exact same data as the dashboard
            Plotly.newPlot('revenue-trends', {charts['revenue_trends']});
            Plotly.newPlot('service-usage', {charts['service_usage']});
            Plotly.newPlot('revenue-distribution', {charts['revenue_distribution']});
            Plotly.newPlot('vip-usage-trends', {charts['vip_usage_trends']});
            Plotly.newPlot('vip-performance', {charts['vip_performance']});
            Plotly.newPlot('vip-service-levels', {charts['vip_service_levels']});
            Plotly.newPlot('dept-billing-trends', {charts['dept_billing_trends']});
            Plotly.newPlot('dept-performance', {charts['dept_performance']});
            Plotly.newPlot('dept-efficiency', {charts['dept_efficiency']});
            Plotly.newPlot('product-revenue-trends', {charts['product_revenue_trends']});
            Plotly.newPlot('product-performance', {charts['product_performance']});
            Plotly.newPlot('product-revenue-distribution', {charts['product_revenue_distribution']});
            Plotly.newPlot('product-churn-analysis', {charts['product_churn_analysis']});
            Plotly.newPlot('complaints-timeline', {charts['complaints_timeline']});
            Plotly.newPlot('complaints-by-type', {charts['complaints_by_type']});
            Plotly.newPlot('resolution-time-distribution', {charts['resolution_time_distribution']});
            Plotly.newPlot('dept-complaints-performance', {charts['dept_complaints_performance']});
            Plotly.newPlot('customer-demographics', {charts['customer_demographics']});
            Plotly.newPlot('customer-behavior', {charts['customer_behavior']});
            Plotly.newPlot('customer-segmentation', {charts['customer_segmentation']});
            Plotly.newPlot('churn-risk-analysis', {charts['churn_risk_analysis']});
            Plotly.newPlot('network-performance-trends', {charts['network_performance_trends']});
            Plotly.newPlot('network-metrics-analysis', {charts['network_metrics_analysis']});
            Plotly.newPlot('bandwidth-utilization', {charts['bandwidth_utilization']});
            Plotly.newPlot('network-health-dashboard', {charts['network_health_dashboard']});
            Plotly.newPlot('operations-performance-trends', {charts['operations_performance_trends']});
            Plotly.newPlot('operations-efficiency-analysis', {charts['operations_efficiency_analysis']});
            Plotly.newPlot('cost-analysis', {charts['cost_analysis']});
            Plotly.newPlot('operations-health-dashboard', {charts['operations_health_dashboard']});
        </script>
    </body>
    </html>
    """
    
    with open('billing_dashboard_report_complete.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Reporte HTML completo generado exitosamente: billing_dashboard_report_complete.html")
    print("📊 Este reporte incluye TODOS los gráficos del dashboard original con los mismos valores")
    print("📧 Se puede enviar por email o abrir en cualquier navegador")
    
    return html_content

if __name__ == "__main__":
    generate_html_report()


