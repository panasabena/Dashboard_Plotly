import dash
from dash import html, dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Generar datos sintéticos (mismo código que en billing_dashboard.py)
def generate_synthetic_data():
    np.random.seed(42)
    
    # 1. Real-time data (últimas 24 horas)
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
    
    # 2. VIP Customers
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
    
    # 3. Departments
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
    
    # 4. Products
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
    
    # 5. Complaints
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
    
    # 6. Customers
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
    
    # 7. Network
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
    
    # 8. Operations
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

# Generar todos los gráficos
def generate_all_charts():
    data = generate_synthetic_data()
    charts = {}
    
    # 1. Real-time Billing Charts
    df = data['real_time']
    
    # Revenue Trends
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['total_revenue'], 
                            mode='lines+markers', name='Total Revenue', line=dict(color='#007bff', width=3)))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['voice_revenue'], 
                            mode='lines+markers', name='Voice Revenue', line=dict(color='#28a745', width=2)))
    fig.update_layout(title="Revenue Trends - Last 24 Hours", height=400)
    charts['revenue_trends'] = fig
    
    # Service Usage by Hour (Subplots)
    fig = go.Figure()
    fig = go.Figure(data=[
        go.Scatter(x=df['timestamp'], y=df['calls_volume'], name='Calls', yaxis='y'),
        go.Scatter(x=df['timestamp'], y=df['messages_volume'], name='Messages', yaxis='y2'),
        go.Scatter(x=df['timestamp'], y=df['data_volume_gb'], name='Data (GB)', yaxis='y3'),
        go.Scatter(x=df['timestamp'], y=df['total_revenue'], name='Revenue ($)', yaxis='y4')
    ])
    fig.update_layout(
        title="Service Usage by Hour",
        yaxis=dict(title="Calls"),
        yaxis2=dict(title="Messages", overlaying='y', side='right'),
        yaxis3=dict(title="Data (GB)", overlaying='y', side='left', position=0.1),
        yaxis4=dict(title="Revenue ($)", overlaying='y', side='right', position=0.9),
        height=400
    )
    charts['service_usage'] = fig
    
    # Revenue Distribution
    total_voice = df['voice_revenue'].sum()
    total_data = df['data_revenue'].sum()
    fig = go.Figure(data=[go.Pie(labels=['Voice Revenue', 'Data Revenue'], 
                                values=[total_voice, total_data], hole=0.4)])
    fig.update_layout(title="Revenue Distribution", height=400)
    charts['revenue_distribution'] = fig
    
    # 2. VIP Customers Charts
    df = data['vip_customers']
    latest_vip = df.groupby('customer_id').last().reset_index()
    
    # VIP Usage Trends
    vip_trends = df.groupby('date').agg({
        'voice_usage_minutes': 'mean',
        'data_usage_gb': 'mean',
        'monthly_bill': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=vip_trends['date'], y=vip_trends['voice_usage_minutes'], 
                            mode='lines+markers', name='Voice Usage (min)', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=vip_trends['date'], y=vip_trends['data_usage_gb'], 
                            mode='lines+markers', name='Data Usage (GB)', line=dict(color='#28a745'), yaxis='y2'))
    fig.add_trace(go.Scatter(x=vip_trends['date'], y=vip_trends['monthly_bill'], 
                            mode='lines+markers', name='Monthly Bill ($)', line=dict(color='#ffc107'), yaxis='y3'))
    fig.update_layout(
        title="VIP Customer Usage Trends",
        yaxis=dict(title="Voice Usage (min)"),
        yaxis2=dict(title="Data Usage (GB)", overlaying='y', side='right'),
        yaxis3=dict(title="Monthly Bill ($)", overlaying='y', side='right', position=0.9),
        height=400
    )
    charts['vip_usage_trends'] = fig
    
    # VIP Performance
    top_10 = latest_vip.nlargest(10, 'monthly_bill')
    fig = go.Figure(data=[go.Bar(x=top_10['customer_id'], y=top_10['monthly_bill'], 
                                marker_color='#007bff')])
    fig.update_layout(title="Top 10 VIP Customers by Monthly Bill", height=400)
    charts['vip_performance'] = fig
    
    # VIP Service Levels
    service_counts = latest_vip['service_level'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=service_counts.index, values=service_counts.values, hole=0.4,
                                marker_colors=['#007bff', '#28a745', '#ffc107'])])
    fig.update_layout(title="VIP Service Level Distribution", height=400)
    charts['vip_service_levels'] = fig
    
    # 3. Department Charts
    df = data['departments']
    latest_dept = df.groupby('department').last().reset_index()
    
    # Department Billing Trends
    dept_trends = df.groupby(['department', 'date'])['billed_amount'].sum().reset_index()
    fig = go.Figure()
    departments = df['department'].unique()
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14', '#20c997']
    
    for i, dept in enumerate(departments):
        dept_data = dept_trends[dept_trends['department'] == dept]
        fig.add_trace(go.Scatter(x=dept_data['date'], y=dept_data['billed_amount'], 
                                mode='lines+markers', name=dept, 
                                line=dict(color=colors[i % len(colors)], width=2)))
    
    fig.update_layout(title="Department Billing Trends - Last 30 Days", height=400)
    charts['dept_billing_trends'] = fig
    
    # Department Performance
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_dept['department'], y=latest_dept['billed_amount'], 
                        name='Billed Amount', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=latest_dept['department'], y=latest_dept['active_users'], 
                        name='Active Users', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Department Performance Comparison", 
                     yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['dept_performance'] = fig
    
    # Department Efficiency
    dept_efficiency = latest_dept.groupby('department')['efficiency_score'].mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=dept_efficiency['department'], 
                                values=dept_efficiency['efficiency_score'], hole=0.4,
                                marker_colors=['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#fd7e14', '#20c997'])])
    fig.update_layout(title="Department Efficiency Distribution", height=400)
    charts['dept_efficiency'] = fig
    
    # 4. Product Charts
    df = data['products']
    latest_products = df.groupby('product').last().reset_index()
    
    # Product Revenue Trends
    product_trends = df.groupby(['product', 'date'])['billed_amount'].sum().reset_index()
    fig = go.Figure()
    products = df['product'].unique()
    colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1']
    
    for i, product in enumerate(products):
        product_data = product_trends[product_trends['product'] == product]
        fig.add_trace(go.Scatter(x=product_data['date'], y=product_data['billed_amount'], 
                                mode='lines+markers', name=product, 
                                line=dict(color=colors[i % len(colors)], width=2)))
    
    fig.update_layout(title="Product Revenue Trends - Last 30 Days", height=400)
    charts['product_revenue_trends'] = fig
    
    # Product Performance
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['billed_amount'], 
                        name='Revenue', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['subscribers'], 
                        name='Subscribers', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Product Performance Comparison", 
                     yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['product_performance'] = fig
    
    # Revenue by Product Category
    fig = go.Figure(data=[go.Pie(labels=latest_products['product'], 
                                values=latest_products['billed_amount'], hole=0.4,
                                marker_colors=['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1'])])
    fig.update_layout(title="Revenue by Product Category", height=400)
    charts['product_revenue_distribution'] = fig
    
    # Churn Rate Analysis
    fig = go.Figure()
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['churn_rate']*100, 
                        name='Churn Rate (%)', marker_color='#dc3545'))
    fig.add_trace(go.Bar(x=latest_products['product'], y=latest_products['profit_margin']*100, 
                        name='Profit Margin (%)', marker_color='#28a745', yaxis='y2'))
    fig.update_layout(title="Churn Rate Analysis by Product", 
                     yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['product_churn_analysis'] = fig
    
    # 5. Complaints Charts
    df = data['complaints']
    
    # Complaints Timeline
    daily_complaints = df.groupby('date').size().reset_index(name='count')
    daily_resolved = df[df['resolved']].groupby('date').size().reset_index(name='resolved_count')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_complaints['date'], y=daily_complaints['count'], 
                            mode='lines+markers', name='Total Complaints', line=dict(color='#dc3545')))
    fig.add_trace(go.Scatter(x=daily_resolved['date'], y=daily_resolved['resolved_count'], 
                            mode='lines+markers', name='Resolved', line=dict(color='#28a745')))
    fig.update_layout(title="Complaints Timeline", height=400)
    charts['complaints_timeline'] = fig
    
    # Complaints by Type and Priority
    complaints_by_type = df.groupby(['complaint_type', 'priority']).size().reset_index(name='count')
    fig = go.Figure()
    for complaint_type in df['complaint_type'].unique():
        type_data = complaints_by_type[complaints_by_type['complaint_type'] == complaint_type]
        fig.add_trace(go.Bar(x=type_data['priority'], y=type_data['count'], name=complaint_type))
    fig.update_layout(title="Complaints by Type and Priority", height=400, barmode='stack')
    charts['complaints_by_type'] = fig
    
    # Resolution Time Distribution
    resolution_bins = pd.cut(df['resolution_time_hours'], bins=[0, 1, 24, 72, float('inf')], 
                            labels=['Same Day', '1-24 Hours', '1-3 Days', '3+ Days'])
    resolution_dist = resolution_bins.value_counts()
    fig = go.Figure(data=[go.Pie(labels=resolution_dist.index, values=resolution_dist.values, hole=0.4,
                                marker_colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545'])])
    fig.update_layout(title="Resolution Time Distribution", height=400)
    charts['resolution_time_distribution'] = fig
    
    # Department Performance in Complaints
    dept_complaints = df.groupby('department').agg({
        'complaint_type': 'count',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=dept_complaints['department'], y=dept_complaints['complaint_type'], 
                        name='Total Complaints', marker_color='#007bff'))
    fig.add_trace(go.Bar(x=dept_complaints['department'], y=dept_complaints['resolution_time_hours'], 
                        name='Avg Resolution Time (h)', marker_color='#ffc107', yaxis='y2'))
    fig.update_layout(title="Department Performance in Complaints", 
                     yaxis2=dict(overlaying='y', side='right'), height=400, barmode='group')
    charts['dept_complaints_performance'] = fig
    
    # 6. Customer Charts
    df = data['customers']
    
    # Customer Demographics Analysis (Subplots)
    fig = go.Figure()
    fig = go.Figure(data=[
        go.Histogram(x=df['age'], name='Age Distribution', nbinsx=20, marker_color='#007bff'),
        go.Bar(x=df['income_level'].value_counts().index, y=df['income_level'].value_counts().values, 
               name='Income Levels', marker_color='#28a745'),
        go.Histogram(x=df['tenure_months'], name='Tenure Distribution', nbinsx=20, marker_color='#ffc107'),
        go.Bar(x=df['region'].value_counts().index, y=df['region'].value_counts().values, 
               name='Regional Distribution', marker_color='#dc3545')
    ])
    fig.update_layout(title="Customer Demographics Analysis", height=400)
    charts['customer_demographics'] = fig
    
    # Customer Behavior Analysis (Subplots)
    fig = go.Figure()
    fig = go.Figure(data=[
        go.Histogram(x=df['monthly_bill'], name='Monthly Bill Distribution', nbinsx=20, marker_color='#007bff'),
        go.Bar(x=df['services_count'].value_counts().index, y=df['services_count'].value_counts().values, 
               name='Services Count', marker_color='#28a745'),
        go.Bar(x=df['payment_method'].value_counts().index, y=df['payment_method'].value_counts().values, 
               name='Payment Methods', marker_color='#ffc107'),
        go.Histogram(x=df['satisfaction_score'], name='Satisfaction Distribution', nbinsx=20, marker_color='#dc3545')
    ])
    fig.update_layout(title="Customer Behavior Analysis", height=400)
    charts['customer_behavior'] = fig
    
    # Customer Segmentation
    df['segment'] = pd.cut(df['monthly_bill'], bins=[0, 100, 200, float('inf')], 
                          labels=['Low Value', 'Medium Value', 'High Value'])
    segment_counts = df['segment'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=segment_counts.index, values=segment_counts.values, hole=0.4,
                                marker_colors=['#ffc107', '#28a745', '#007bff'])])
    fig.update_layout(title="Customer Segmentation", height=400)
    charts['customer_segmentation'] = fig
    
    # Churn Risk Analysis
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=df['churn_risk'], name='Churn Risk Distribution', nbinsx=20, marker_color='#dc3545'))
    fig.add_trace(go.Scatter(x=df['monthly_bill'], y=df['churn_risk'], mode='markers', 
                            name='Risk vs Bill', marker_color='#007bff', yaxis='y2'))
    fig.update_layout(title="Churn Risk Analysis", yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['churn_risk_analysis'] = fig
    
    # 7. Network Charts
    df = data['network']
    
    # Network Performance Trends
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['traffic_volume_gbps'], 
                            mode='lines+markers', name='Traffic Volume (Gbps)', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['connection_speed_mbps'], 
                            mode='lines+markers', name='Connection Speed (Mbps)', line=dict(color='#28a745'), yaxis='y2'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['latency_ms'], 
                            mode='lines+markers', name='Latency (ms)', line=dict(color='#dc3545'), yaxis='y3'))
    fig.update_layout(
        title="Network Performance Trends",
        yaxis=dict(title="Traffic Volume (Gbps)"),
        yaxis2=dict(title="Connection Speed (Mbps)", overlaying='y', side='right'),
        yaxis3=dict(title="Latency (ms)", overlaying='y', side='right', position=0.9),
        height=400
    )
    charts['network_performance_trends'] = fig
    
    # Network Metrics Analysis
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['active_connections'], 
                            mode='lines+markers', name='Active Connections', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['packet_loss_percentage'], 
                            mode='lines+markers', name='Packet Loss (%)', line=dict(color='#dc3545'), yaxis='y2'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['bandwidth_utilization'], 
                            mode='lines+markers', name='Bandwidth Utilization (%)', line=dict(color='#ffc107'), yaxis='y3'))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['uptime_percentage'], 
                            mode='lines+markers', name='Uptime (%)', line=dict(color='#28a745'), yaxis='y4'))
    fig.update_layout(
        title="Network Metrics Analysis",
        yaxis=dict(title="Active Connections"),
        yaxis2=dict(title="Packet Loss (%)", overlaying='y', side='right'),
        yaxis3=dict(title="Bandwidth Utilization (%)", overlaying='y', side='right', position=0.9),
        yaxis4=dict(title="Uptime (%)", overlaying='y', side='right', position=0.8),
        height=400
    )
    charts['network_metrics_analysis'] = fig
    
    # Bandwidth Utilization
    bandwidth_bins = pd.cut(df['bandwidth_utilization'], bins=[0, 30, 60, 80, 100], 
                           labels=['Low', 'Medium', 'High', 'Critical'])
    bandwidth_dist = bandwidth_bins.value_counts()
    fig = go.Figure(data=[go.Pie(labels=bandwidth_dist.index, values=bandwidth_dist.values, hole=0.4,
                                marker_colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545'])])
    fig.update_layout(title="Bandwidth Utilization", height=400)
    charts['bandwidth_utilization'] = fig
    
    # Network Health Dashboard
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['uptime_percentage'], 
                            mode='lines+markers', name='Uptime (%)', line=dict(color='#28a745')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['packet_loss_percentage']*10, 
                            mode='lines+markers', name='Packet Loss (x10)', line=dict(color='#dc3545'), yaxis='y2'))
    fig.update_layout(title="Network Health Dashboard", 
                     yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['network_health_dashboard'] = fig
    
    # 8. Operations Charts
    df = data['operations']
    
    # Operations Performance Trends
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['invoices_processed'], 
                            mode='lines+markers', name='Invoices Processed', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=df['date'], y=df['processing_time_minutes'], 
                            mode='lines+markers', name='Processing Time (min)', line=dict(color='#ffc107'), yaxis='y2'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['automation_rate']*100, 
                            mode='lines+markers', name='Automation Rate (%)', line=dict(color='#28a745'), yaxis='y3'))
    fig.update_layout(
        title="Operations Performance Trends",
        yaxis=dict(title="Invoices Processed"),
        yaxis2=dict(title="Processing Time (min)", overlaying='y', side='right'),
        yaxis3=dict(title="Automation Rate (%)", overlaying='y', side='right', position=0.9),
        height=400
    )
    charts['operations_performance_trends'] = fig
    
    # Operations Efficiency Analysis
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['staff_productivity']*100, 
                            mode='lines+markers', name='Staff Productivity (%)', line=dict(color='#007bff')))
    fig.add_trace(go.Scatter(x=df['date'], y=df['error_rate']*100, 
                            mode='lines+markers', name='Error Rate (%)', line=dict(color='#dc3545'), yaxis='y2'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['cost_per_invoice'], 
                            mode='lines+markers', name='Cost per Invoice ($)', line=dict(color='#ffc107'), yaxis='y3'))
    fig.add_trace(go.Scatter(x=df['date'], y=df['customer_satisfaction'], 
                            mode='lines+markers', name='Customer Satisfaction', line=dict(color='#28a745'), yaxis='y4'))
    fig.update_layout(
        title="Operations Efficiency Analysis",
        yaxis=dict(title="Staff Productivity (%)"),
        yaxis2=dict(title="Error Rate (%)", overlaying='y', side='right'),
        yaxis3=dict(title="Cost per Invoice ($)", overlaying='y', side='right', position=0.9),
        yaxis4=dict(title="Customer Satisfaction", overlaying='y', side='right', position=0.8),
        height=400
    )
    charts['operations_efficiency_analysis'] = fig
    
    # Cost Analysis by Operation
    cost_bins = pd.cut(df['cost_per_invoice'], bins=[0, 3, 5, 7, float('inf')], 
                      labels=['Low', 'Medium', 'High', 'Very High'])
    cost_dist = cost_bins.value_counts()
    fig = go.Figure(data=[go.Pie(labels=cost_dist.index, values=cost_dist.values, hole=0.4,
                                marker_colors=['#28a745', '#ffc107', '#fd7e14', '#dc3545'])])
    fig.update_layout(title="Cost Analysis by Operation", height=400)
    charts['cost_analysis'] = fig
    
    # Operations Health Dashboard
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['automation_rate']*100, 
                            mode='lines+markers', name='Automation Rate (%)', line=dict(color='#28a745')))
    fig.add_trace(go.Scatter(x=df['date'], y=df['error_rate']*100, 
                            mode='lines+markers', name='Error Rate (%)', line=dict(color='#dc3545'), yaxis='y2'))
    fig.update_layout(title="Operations Health Dashboard", 
                     yaxis2=dict(overlaying='y', side='right'), height=400)
    charts['operations_health_dashboard'] = fig
    
    return charts

# Generar HTML estático
def generate_html_report():
    data = generate_synthetic_data()
    charts = generate_all_charts()
    
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
                    <h3>{data['network']['uptime_percentage'].mean():.1f}%</h3>
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
                    <h3>{data['operations']['automation_rate'].mean():.1%}</h3>
                    <p>Automation Rate</p>
                </div>
                <div class="metric">
                    <h3>{data['operations']['error_rate'].mean():.1%}</h3>
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
            <p>📊 This report was generated automatically on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>All data is synthetic and for demonstration purposes</p>
        </div>
        
        <script>
            // Render all charts
            Plotly.newPlot('revenue-trends', {charts['revenue_trends'].to_json()});
            Plotly.newPlot('service-usage', {charts['service_usage'].to_json()});
            Plotly.newPlot('revenue-distribution', {charts['revenue_distribution'].to_json()});
            Plotly.newPlot('vip-usage-trends', {charts['vip_usage_trends'].to_json()});
            Plotly.newPlot('vip-performance', {charts['vip_performance'].to_json()});
            Plotly.newPlot('vip-service-levels', {charts['vip_service_levels'].to_json()});
            Plotly.newPlot('dept-billing-trends', {charts['dept_billing_trends'].to_json()});
            Plotly.newPlot('dept-performance', {charts['dept_performance'].to_json()});
            Plotly.newPlot('dept-efficiency', {charts['dept_efficiency'].to_json()});
            Plotly.newPlot('product-revenue-trends', {charts['product_revenue_trends'].to_json()});
            Plotly.newPlot('product-performance', {charts['product_performance'].to_json()});
            Plotly.newPlot('product-revenue-distribution', {charts['product_revenue_distribution'].to_json()});
            Plotly.newPlot('product-churn-analysis', {charts['product_churn_analysis'].to_json()});
            Plotly.newPlot('complaints-timeline', {charts['complaints_timeline'].to_json()});
            Plotly.newPlot('complaints-by-type', {charts['complaints_by_type'].to_json()});
            Plotly.newPlot('resolution-time-distribution', {charts['resolution_time_distribution'].to_json()});
            Plotly.newPlot('dept-complaints-performance', {charts['dept_complaints_performance'].to_json()});
            Plotly.newPlot('customer-demographics', {charts['customer_demographics'].to_json()});
            Plotly.newPlot('customer-behavior', {charts['customer_behavior'].to_json()});
            Plotly.newPlot('customer-segmentation', {charts['customer_segmentation'].to_json()});
            Plotly.newPlot('churn-risk-analysis', {charts['churn_risk_analysis'].to_json()});
            Plotly.newPlot('network-performance-trends', {charts['network_performance_trends'].to_json()});
            Plotly.newPlot('network-metrics-analysis', {charts['network_metrics_analysis'].to_json()});
            Plotly.newPlot('bandwidth-utilization', {charts['bandwidth_utilization'].to_json()});
            Plotly.newPlot('network-health-dashboard', {charts['network_health_dashboard'].to_json()});
            Plotly.newPlot('operations-performance-trends', {charts['operations_performance_trends'].to_json()});
            Plotly.newPlot('operations-efficiency-analysis', {charts['operations_efficiency_analysis'].to_json()});
            Plotly.newPlot('cost-analysis', {charts['cost_analysis'].to_json()});
            Plotly.newPlot('operations-health-dashboard', {charts['operations_health_dashboard'].to_json()});
        </script>
    </body>
    </html>
    """
    
    # Guardar el archivo HTML
    with open('billing_dashboard_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Reporte HTML generado exitosamente: billing_dashboard_report.html")
    print("📧 Este archivo se puede enviar por email o abrir en cualquier navegador")
    
    return html_content

if __name__ == "__main__":
    generate_html_report()
