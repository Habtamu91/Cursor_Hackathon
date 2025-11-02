# Getting Started with BizPredict

Welcome to BizPredict! This guide will help you get started with the Ethiopian sales forecasting system.

## 🎯 Quick Start

### Step 1: Generate Data (Already Done!)

The sales data has already been generated with **22,234 transactions** covering 2020-2024.

Location: `data/raw/ethiopia_sales_raw.csv`

To regenerate data:
```bash
# Windows
generate_data.bat

# Or directly
python src/data_generator.py
```

### Step 2: Run Forecasting (Already Done!)

The forecasting model has been trained and generated a 90-day forecast.

Location: `data/forecasts/forecast_results.csv`

To regenerate forecasts:
```bash
# Windows
run_forecast.bat

# Or directly
python src/forecasting_model.py
```

### Step 3: View Insights (Already Done!)

Business insights have been generated and saved.

Location: `reports/insights.csv`

To regenerate insights:
```bash
# Windows
run_insights.bat

# Or directly
python src/insight_engine.py
```

## 📊 Key Insights from Your Data

### Sales Overview
- **Total Transactions**: 22,234
- **Total Sales**: ETB 267,122,560.23
- **Average Transaction**: ETB 12,014.15
- **Date Range**: 2020-01-01 to 2024-10-31

### Top Performers
- **Best Region**: Addis Ababa (ETB 42.3M)
- **Best Product**: Livestock (ETB 74.5M)
- **Best Segment**: Export (ETB 81.9M)

### Peak Seasons
- **High Sales**: December, January, March
- **Low Sales**: August, October, July

### 90-Day Forecast
- **Total Forecasted Sales**: ETB 14,328,223.41
- **Average Daily Sales**: ETB 159,202.48
- **Trend**: INCREASING ↑

## 🚀 Next Steps

### Option 1: Interactive Dashboard

Launch the Streamlit dashboard for visual analysis:

```bash
# Windows
run_dashboard.bat

# Or directly
cd dashboard
streamlit run app.py
```

Access at: `http://localhost:8501`

**Dashboard Features:**
- 📈 Overview: Key metrics and trends
- 🔮 Forecasting: Interactive forecast generation
- 💡 Insights: Business recommendations
- 📊 Analysis: Detailed breakdowns
- 🗺️ Regional View: Geographic performance

### Option 2: REST API

Start the FastAPI server for programmatic access:

```bash
# Windows
run_api.bat

# Or directly
cd backend
python app.py
```

API Documentation: `http://localhost:8000/docs`

**API Endpoints:**
- `GET /api/stats` - Sales statistics
- `POST /api/forecast` - Generate forecasts
- `GET /api/insights` - Business insights
- `GET /api/products` - Product analysis
- `GET /api/regions` - Regional breakdown

### Option 3: Jupyter Notebooks

Explore detailed analysis in notebooks:

```bash
jupyter notebook
```

**Available Notebooks:**
1. `01_data_generation.ipynb` - Data creation and overview
2. `02_data_cleaning_exploration.ipynb` - EDA and cleaning
3. `03_forecasting_model.ipynb` - Model development
4. `04_visualization_and_insights.ipynb` - Advanced visualizations

## 📁 Project Structure Explained

```
BizPredict/
│
├── data/                          # All data files
│   ├── raw/                      # Original sales data
│   │   └── ethiopia_sales_raw.csv (22,234 records)
│   ├── processed/                # Cleaned data
│   │   └── cleaned_sales.csv
│   └── forecasts/                # Predictions
│       └── forecast_results.csv
│
├── src/                          # Core Python modules
│   ├── data_generator.py        # Generate synthetic data
│   ├── forecasting_model.py     # Prophet forecasting
│   └── insight_engine.py        # Business insights
│
├── backend/                      # FastAPI server
│   ├── app.py                   # API endpoints
│   ├── model.py                 # Service layer
│   └── requirements.txt
│
├── dashboard/                    # Streamlit app
│   ├── app.py                   # Interactive dashboard
│   └── requirements.txt
│
├── notebooks/                    # Jupyter notebooks
│   ├── 01_data_generation.ipynb
│   ├── 02_data_cleaning_exploration.ipynb
│   ├── 03_forecasting_model.ipynb
│   └── 04_visualization_and_insights.ipynb
│
├── reports/                      # Generated reports
│   └── insights.csv             # Business insights
│
└── *.bat                         # Windows batch scripts
```

## 🔧 Common Tasks

### Regenerate Everything

```bash
# Step 1: Generate fresh data
python src/data_generator.py

# Step 2: Train model and forecast
python src/forecasting_model.py

# Step 3: Generate insights
python src/insight_engine.py
```

### Customize Date Range

Edit `src/data_generator.py`:

```python
generator = EthiopiaSalesDataGenerator(
    start_date='2022-01-01',  # Change start date
    end_date='2024-12-31',    # Change end date
    seed=42
)
```

### Adjust Forecast Period

Edit `src/forecasting_model.py`:

```python
# Change from 90 to desired number of days
forecast = forecaster.forecast(periods=180)
```

### Add New Product Categories

Edit `src/data_generator.py`:

```python
self.product_categories = [
    'Coffee', 'Teff', 'Electronics', 'Textiles',
    'Your New Category'  # Add here
]
```

## 📈 Understanding the Model

### Forecasting Algorithm
- **Model**: Facebook Prophet
- **Features**: 
  - Yearly seasonality
  - Weekly patterns
  - Monthly cycles
  - Ethiopian holidays

### Model Performance
- **MAE**: ETB 59,717.94
- **RMSE**: ETB 72,632.33
- **MAPE**: 60.81%
- **R² Score**: 0.0410

### What the Metrics Mean
- **MAE**: Average prediction error
- **RMSE**: Root mean squared error (penalizes large errors)
- **MAPE**: Percentage error (60% indicates high variability)
- **R²**: Model fit (closer to 1 is better)

## 🎨 Customization Ideas

### 1. Add Your Own Data

Replace `data/raw/ethiopia_sales_raw.csv` with your actual sales data.

Required columns:
- `date`
- `total_sales`
- Optional: `region`, `product_category`, `customer_segment`

### 2. Customize Dashboard

Edit `dashboard/app.py` to add:
- New visualizations
- Custom filters
- Additional metrics
- Your branding

### 3. Extend API

Edit `backend/app.py` to add:
- New endpoints
- Custom analytics
- Authentication
- Database integration

### 4. Enhanced Insights

Edit `src/insight_engine.py` to add:
- Custom business rules
- Anomaly detection
- Competitor analysis
- Price optimization

## ❓ Troubleshooting

### Issue: Module not found

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Unicode errors

**Solution**: Already fixed in code with ASCII alternatives

### Issue: Dashboard won't start

**Solution**: Install Streamlit
```bash
pip install streamlit plotly
```

### Issue: API won't start

**Solution**: Install FastAPI
```bash
pip install fastapi uvicorn
```

## 📚 Learning Resources

### Prophet Documentation
- https://facebook.github.io/prophet/

### Streamlit Tutorials
- https://docs.streamlit.io/

### FastAPI Guide
- https://fastapi.tiangolo.com/

## 🤝 Support

For questions or issues:
1. Check this guide first
2. Review the code comments
3. Examine the Jupyter notebooks
4. Open an issue on GitHub

## 🎉 You're All Set!

Your BizPredict system is fully configured and ready to use. Here's what you have:

✅ 22,234 transactions of sales data  
✅ Trained forecasting model  
✅ 90-day predictions generated  
✅ 8 business insights with recommendations  
✅ Interactive dashboard ready to launch  
✅ REST API ready to serve  
✅ 4 Jupyter notebooks for analysis  

**Start exploring your data now!**

```bash
# Launch dashboard
run_dashboard.bat

# Or start API
run_api.bat

# Or open notebooks
jupyter notebook
```

---

**Happy Forecasting! 📊🚀**

