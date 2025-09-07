# 🚀 Deploy to Render - Billing Dashboard

## 📋 Prerequisites

1. **GitHub Repository**: Your code must be in a GitHub repository
2. **Render Account**: Create a free account at [render.com](https://render.com)
3. **Repository Access**: Make sure your repository is public or connected to Render

## 🔧 Deployment Steps

### 1. Create New Web Service on Render

1. Go to [render.com](https://render.com) and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account if not already connected
4. Select your repository: `panasabena/Dashboard_Plotly`

### 2. Configure the Service

**Basic Settings:**
- **Name**: `charter-billing-dashboard` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
- **Start Command**: `gunicorn billing_dashboard:server --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

**Advanced Settings:**
- **Python Version**: `3.12.9` (specified in runtime.txt and pyproject.toml)
- **Auto-Deploy**: `Yes` (recommended for automatic updates)

**IMPORTANT**: If Render still uses Python 3.13, manually set the Python version in the Render dashboard:
1. Go to your service → **Settings** → **Environment**
2. Add environment variable: `PYTHON_VERSION` = `3.12.9`
3. Or use the `render.yaml` file for automatic configuration

### 3. Environment Variables (Optional)

If your dashboard needs any environment variables, add them in the Render dashboard:
- Go to your service → **Environment**
- Add any required variables

### 4. Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your application using the Procfile
   - Provide you with a public URL

## 🌐 Access Your Dashboard

Once deployed, you'll get a URL like:
```
https://charter-billing-dashboard.onrender.com
```

## 📊 Dashboard Features

Your deployed dashboard includes:

### 📈 **Billing Operations Dashboard**
- **Revenue Analytics**: Monthly revenue trends and forecasts
- **Customer Metrics**: Active customers, churn analysis, and growth
- **Service Performance**: Network health, service quality metrics
- **Financial Health**: Revenue vs. costs, profitability analysis

### 🎨 **Modern UI Features**
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Interactive Charts**: Plotly-powered visualizations
- **Real-time Updates**: Dynamic data refresh
- **Professional Styling**: Bootstrap-based modern interface

## 🔧 Troubleshooting

### Common Issues:

1. **Python Version Issues**: If Render uses Python 3.13 instead of 3.12:
   - ✅ **SOLVED**: Added multiple Python version specifications
   - **Manual Fix**: Set `PYTHON_VERSION=3.12.9` in Render environment variables
   - **Files Updated**: runtime.txt, pyproject.toml, render.yaml, .python-version

2. **Numpy/Scikit-learn Build Errors**: If you see numpy compilation errors:
   - ✅ **SOLVED**: Updated to numpy 2.0.2 and scikit-learn 1.5.0 (Python 3.13 compatible)
   - The error was caused by version incompatibilities

3. **Build Fails**: Check that all dependencies are in `requirements.txt`
4. **App Won't Start**: Verify the Procfile command is correct
5. **Port Issues**: Render automatically sets the PORT environment variable
6. **Memory Issues**: Free tier has memory limits; consider upgrading if needed

### Logs:
- Check the **Logs** tab in your Render service dashboard
- Look for error messages during build or runtime

### If You Still Get Pandas Errors:
1. Make sure you're using Python 3.12.0 (specified in runtime.txt)
2. Verify the build command includes: `pip install --upgrade pip`
3. Check that pandas version is 2.2.3 or higher in requirements.txt

## 💰 Pricing

- **Free Tier**: 750 hours/month, sleeps after 15 minutes of inactivity
- **Starter Plan**: $7/month for always-on service
- **Professional**: $25/month for production use

## 🔄 Updates

To update your dashboard:
1. Push changes to your GitHub repository
2. Render will automatically redeploy (if auto-deploy is enabled)
3. Or manually trigger deployment from the Render dashboard

## 📞 Support

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **Community**: [render.com/community](https://render.com/community)
- **Status Page**: [status.render.com](https://status.render.com)

---

**🎉 Your Charter Spectrum Billing Dashboard is now live!**
