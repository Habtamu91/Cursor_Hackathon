# BizPredict – Smart Business Forecasting Assistant

A comprehensive machine learning-powered forecasting system for Ethiopian business sales data. This project provides end-to-end capabilities for data generation, analysis, forecasting, and interactive visualization.

## 🚀 Features

- **Synthetic Data Generation**: Creates realistic Ethiopian sales data with regional, seasonal, and product variations
- **Advanced Forecasting**: Uses Facebook Prophet for accurate time series predictions
- **Business Insights**: Automatically generates actionable recommendations
- **Interactive Dashboard**: Streamlit-based visualization interface
- **REST API**: FastAPI backend for model serving
- **Comprehensive Analysis**: Jupyter notebooks for exploratory data analysis

## 📁 Project Structure

```
BizPredict/
├── backend/                    # FastAPI backend
│   ├── app.py                 # API endpoints
│   ├── model.py               # Forecasting service
│   └── requirements.txt       # Backend dependencies
├── dashboard/                  # Streamlit dashboard
│   ├── app.py                 # Interactive dashboard
│   └── requirements.txt       # Dashboard dependencies
├── data/                       # Data directory
│   ├── raw/                   # Raw sales data
│   ├── processed/             # Cleaned data
│   └── forecasts/             # Forecast results
├── notebooks/                  # Jupyter notebooks
│   ├── 01_data_generation.ipynb
│   ├── 02_data_cleaning_exploration.ipynb
│   ├── 03_forecasting_model.ipynb
│   └── 04_visualization_and_insights.ipynb
├── reports/                    # Generated reports
├── src/                        # Source code
│   ├── data_generator.py      # Data generation module
│   ├── forecasting_model.py   # Forecasting models
│   └── insight_engine.py      # Business insights
└── README.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.9+
- pip

### Setup

1. Clone the repository:
```bash
cd BizPredict
```

2. Install dependencies:
```bash
# For data generation and analysis
pip install pandas numpy prophet scikit-learn matplotlib seaborn jupyter

# For backend API
pip install -r backend/requirements.txt

# For dashboard
pip install -r dashboard/requirements.txt
```

## 📊 Quick Start

### 1. Generate Sales Data

```bash
python src/data_generator.py
```

This creates `data/raw/ethiopia_sales_raw.csv` with synthetic sales data.

### 2. Train Forecasting Model

```bash
python src/forecasting_model.py
```

Trains Prophet model and generates forecasts.

### 3. Generate Business Insights

```bash
python src/insight_engine.py
```

Analyzes data and produces actionable recommendations.

### 4. Run Interactive Dashboard

```bash
cd dashboard
streamlit run app.py
```

Access the dashboard at `http://localhost:8501`

### 5. Start API Server

```bash
cd backend
python app.py
```

API documentation available at `http://localhost:8000/docs`

## 📓 Jupyter Notebooks

Explore the notebooks for detailed analysis:

```bash
jupyter notebook
```

1. **01_data_generation.ipynb**: Data generation and initial exploration
2. **02_data_cleaning_exploration.ipynb**: Data cleaning and EDA
3. **03_forecasting_model.ipynb**: Model training and evaluation
4. **04_visualization_and_insights.ipynb**: Advanced visualizations

## 🔮 Usage Examples

### Python API

```python
from src.forecasting_model import SalesForecaster

# Load data and train model
forecaster = SalesForecaster()
forecaster.prepare_data(df, test_size=90)
forecaster.train_model()

# Generate 90-day forecast
forecast = forecaster.forecast(periods=90)

# Evaluate model
metrics = forecaster.evaluate_model()
```

### REST API

```bash
# Get sales statistics
curl http://localhost:8000/api/stats

# Generate forecast
curl -X POST http://localhost:8000/api/forecast \
  -H "Content-Type: application/json" \
  -d '{"periods": 90}'

# Get business insights
curl http://localhost:8000/api/insights
```

## 📈 Key Features

### Data Generation
- **Ethiopian Context**: 8 regions, 10 product categories
- **Realistic Patterns**: Seasonality, trends, and noise
- **Holiday Effects**: Ethiopian holidays (Timkat, Meskel, New Year)
- **Customer Segments**: Retail, Wholesale, Export, B2B, Direct

### Forecasting Model
- **Algorithm**: Facebook Prophet with custom seasonality
- **Features**: Yearly, monthly, and weekly patterns
- **Evaluation Metrics**: MAE, RMSE, MAPE, R²
- **Forecast Horizon**: Flexible (30, 60, 90, 180 days)

### Business Insights
- Growth trend analysis
- Seasonality patterns
- Product performance
- Regional comparisons
- Customer segment analysis
- Actionable recommendations

## 🎯 Use Cases

- **Inventory Planning**: Forecast demand for better stock management
- **Sales Strategy**: Identify peak periods and optimize campaigns
- **Regional Analysis**: Compare performance across Ethiopian regions
- **Product Mix**: Optimize product portfolio based on trends
- **Resource Allocation**: Plan staffing and resources based on predictions

## 📊 Dataset

The synthetic dataset includes:
- **Time Range**: 2020-01-01 to 2024-10-31
- **Transactions**: 50,000+ records
- **Regions**: Addis Ababa, Oromia, Amhara, Tigray, SNNPR, Somali, Afar, Dire Dawa
- **Products**: Coffee, Teff, Electronics, Textiles, Spices, Livestock, Vegetables, Injera, Leather Goods, Cereals
- **Currency**: Ethiopian Birr (ETB)

## 🧪 Model Performance

Typical model metrics:
- **MAE**: ~15,000 ETB
- **RMSE**: ~20,000 ETB
- **MAPE**: 8-12%
- **R²**: 0.85-0.92

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests.

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

BizPredict Development Team

## 📧 Contact

For questions and support, please open an issue on GitHub.

## 🙏 Acknowledgments

- Facebook Prophet for time series forecasting
- Streamlit for rapid dashboard development
- FastAPI for modern API development
- Ethiopian business community for inspiration

---

**Built with ❤️ for Ethiopian businesses**