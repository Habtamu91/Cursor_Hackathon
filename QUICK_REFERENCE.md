# BizPredict Quick Reference Card

## 🚀 Launch Commands

| Action | Windows Batch | Python Command |
|--------|--------------|----------------|
| Generate Data | `generate_data.bat` | `python src/data_generator.py` |
| Run Forecast | `run_forecast.bat` | `python src/forecasting_model.py` |
| Generate Insights | `run_insights.bat` | `python src/insight_engine.py` |
| Start Dashboard | `run_dashboard.bat` | `streamlit run dashboard/app.py` |
| Start API | `run_api.bat` | `python backend/app.py` |
| Open Notebooks | - | `jupyter notebook` |

## 📁 Key File Locations

| Data Type | Location |
|-----------|----------|
| Raw Sales Data | `data/raw/ethiopia_sales_raw.csv` |
| Cleaned Data | `data/processed/cleaned_sales.csv` |
| Forecasts | `data/forecasts/forecast_results.csv` |
| Insights | `reports/insights.csv` |

## 📊 Current Data Stats

| Metric | Value |
|--------|-------|
| Total Transactions | 22,234 |
| Date Range | 2020-01-01 to 2024-10-31 |
| Total Sales | ETB 267,122,560.23 |
| Average Transaction | ETB 12,014.15 |
| Forecast Period | 90 days |
| Forecasted Sales | ETB 14,328,223.41 |
| Total Insights | 8 |

## 🌍 Ethiopian Context

### Regions (8)
Addis Ababa, Oromia, Amhara, Tigray, SNNPR, Somali, Afar, Dire Dawa

### Products (10)
Coffee, Teff, Electronics, Textiles, Spices, Livestock, Vegetables, Injera, Leather Goods, Cereals

### Customer Segments (5)
Retail, Wholesale, Export, B2B, Direct Consumer

## 📈 Top Performers

| Category | Winner | Sales (ETB) |
|----------|--------|-------------|
| Best Region | Addis Ababa | 42,307,050.12 |
| Best Product | Livestock | 74,509,057.73 |
| Best Segment | Export | 81,942,705.07 |

## 📅 Seasonality

| Period | Months |
|--------|--------|
| Peak Sales | December, January, March |
| Low Sales | August, October, July |

## 🔗 URLs

| Service | URL | Port |
|---------|-----|------|
| Dashboard | http://localhost:8501 | 8501 |
| API | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |

## 🛠️ API Endpoints

```
GET  /                    - Welcome message
GET  /health             - Health check
GET  /api/stats          - Sales statistics
POST /api/forecast       - Generate forecast
GET  /api/insights       - Business insights
GET  /api/products       - Product stats
GET  /api/regions        - Regional stats
GET  /api/trends         - Sales trends
GET  /api/categories     - Product categories
GET  /api/historical     - Historical data
```

## 📦 Python Modules

| Module | Purpose |
|--------|---------|
| `src/data_generator.py` | Generate synthetic sales data |
| `src/forecasting_model.py` | Train and forecast with Prophet |
| `src/insight_engine.py` | Generate business insights |
| `backend/app.py` | FastAPI application |
| `backend/model.py` | Forecasting service |
| `dashboard/app.py` | Streamlit dashboard |

## 📓 Notebooks

1. `01_data_generation.ipynb` - Generate and explore data
2. `02_data_cleaning_exploration.ipynb` - Clean and analyze
3. `03_forecasting_model.ipynb` - Train and evaluate model
4. `04_visualization_and_insights.ipynb` - Visualize and report

## 💻 Code Snippets

### Generate Data
```python
from src.data_generator import EthiopiaSalesDataGenerator

generator = EthiopiaSalesDataGenerator()
df = generator.save_data()
```

### Train Forecast Model
```python
from src.forecasting_model import SalesForecaster

forecaster = SalesForecaster()
forecaster.prepare_data(df, test_size=90)
forecaster.train_model()
forecast = forecaster.forecast(periods=90)
```

### Generate Insights
```python
from src.insight_engine import InsightEngine

engine = InsightEngine(df)
insights = engine.generate_all_insights()
engine.display_insights()
```

### API Request
```python
import requests

# Get stats
response = requests.get('http://localhost:8000/api/stats')
stats = response.json()

# Generate forecast
forecast = requests.post(
    'http://localhost:8000/api/forecast',
    json={'periods': 90}
)
```

## 🔧 Configuration

### Change Date Range
Edit `src/data_generator.py`:
```python
generator = EthiopiaSalesDataGenerator(
    start_date='2022-01-01',
    end_date='2024-12-31'
)
```

### Change Forecast Period
Edit function call:
```python
forecast = forecaster.forecast(periods=180)  # 180 days
```

### Add Products
Edit `src/data_generator.py`:
```python
self.product_categories = [
    'Coffee', 'Teff', 'Your Product'
]
```

## 📚 Dependencies

Core packages:
- pandas
- numpy
- prophet
- scikit-learn
- matplotlib
- seaborn
- plotly
- fastapi
- uvicorn
- streamlit
- jupyter

Install all:
```bash
pip install -r requirements.txt
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not found | `pip install -r requirements.txt` |
| Dashboard won't start | `pip install streamlit plotly` |
| API won't start | `pip install fastapi uvicorn` |
| Unicode errors | Already fixed with ASCII alternatives |
| Prophet errors | `pip install prophet` |

## ⌨️ Keyboard Shortcuts (Dashboard)

| Key | Action |
|-----|--------|
| `R` | Rerun dashboard |
| `C` | Clear cache |
| `?` | Show help |

## 📋 Project Structure

```
BizPredict/
├── data/           # All data files
├── src/            # Python modules
├── backend/        # API server
├── dashboard/      # Web interface
├── notebooks/      # Jupyter notebooks
├── reports/        # Generated reports
├── *.bat           # Batch scripts
└── *.md            # Documentation
```

## ✅ Checklist

- [x] Data generated (22,234 records)
- [x] Model trained
- [x] Forecasts created (90 days)
- [x] Insights generated (8 insights)
- [x] API ready
- [x] Dashboard ready
- [x] Notebooks created
- [x] Documentation complete

## 🎯 Next Actions

1. **View Dashboard**: Run `run_dashboard.bat`
2. **Explore API**: Run `run_api.bat` → Visit http://localhost:8000/docs
3. **Analyze Data**: Run `jupyter notebook`
4. **Regenerate**: Run any `run_*.bat` script

## 📞 Support

1. Check `GETTING_STARTED.md` for detailed guide
2. Check `PROJECT_SUMMARY.md` for overview
3. Check `README.md` for documentation
4. Review code comments
5. Open GitHub issue

---

**BizPredict v1.0 | November 2025**

