"""
Forecasting Service Backend
Handles data loading, model training, and predictions
"""

import pandas as pd
import numpy as np
from prophet import Prophet
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class ForecastingService:
    """Service for managing forecasting operations"""
    
    def __init__(self, data_path='data/raw/ethiopia_sales_raw.csv'):
        self.data_path = data_path
        self.df = None
        self.model = None
        self.data_loaded = False
        self.model_trained = False
        
    def load_data(self):
        """Load sales data"""
        try:
            self.df = pd.read_csv(self.data_path)
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.data_loaded = True
            print(f"✓ Loaded {len(self.df)} transactions")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data_loaded = False
            
    def train_model(self):
        """Train Prophet forecasting model"""
        if not self.data_loaded:
            raise ValueError("Data not loaded")
        
        # Aggregate daily sales
        df_daily = self.df.groupby('date')['total_sales'].sum().reset_index()
        df_daily.columns = ['ds', 'y']
        
        # Initialize and train model
        self.model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05,
            seasonality_mode='multiplicative'
        )
        
        # Add custom seasonality
        self.model.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        )
        
        self.model.fit(df_daily)
        self.model_trained = True
        print("✓ Model trained successfully")
        
    def generate_forecast(self, periods=90, category=None, region=None):
        """
        Generate forecast with optional filters
        
        Args:
            periods: Number of days to forecast
            category: Optional product category filter
            region: Optional region filter
            
        Returns:
            Dictionary with forecast data
        """
        if not self.model_trained:
            raise ValueError("Model not trained")
        
        # Filter data if needed
        df_filtered = self.df.copy()
        if category:
            df_filtered = df_filtered[df_filtered['product_category'] == category]
        if region:
            df_filtered = df_filtered[df_filtered['region'] == region]
        
        # If filtered, retrain on subset
        if category or region:
            df_daily = df_filtered.groupby('date')['total_sales'].sum().reset_index()
            df_daily.columns = ['ds', 'y']
            
            temp_model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                changepoint_prior_scale=0.05,
                seasonality_mode='multiplicative'
            )
            temp_model.fit(df_daily)
            model = temp_model
        else:
            model = self.model
        
        # Generate forecast
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        
        # Get future predictions only
        forecast_future = forecast.iloc[-periods:]
        
        # Calculate metrics on historical data
        historical = forecast.iloc[:-periods]
        df_daily = df_filtered.groupby('date')['total_sales'].sum().reset_index()
        
        if len(historical) > 0 and len(df_daily) > 0:
            mae = np.mean(np.abs(historical['yhat'].values - df_daily['total_sales'].values))
            mape = np.mean(np.abs((df_daily['total_sales'].values - historical['yhat'].values) / df_daily['total_sales'].values)) * 100
        else:
            mae = 0
            mape = 0
        
        return {
            'dates': forecast_future['ds'].dt.strftime('%Y-%m-%d').tolist(),
            'predictions': forecast_future['yhat'].round(2).tolist(),
            'lower_bound': forecast_future['yhat_lower'].round(2).tolist(),
            'upper_bound': forecast_future['yhat_upper'].round(2).tolist(),
            'metrics': {
                'mae': float(mae),
                'mape': float(mape),
                'total_forecast': float(forecast_future['yhat'].sum()),
                'avg_daily': float(forecast_future['yhat'].mean())
            }
        }
    
    def get_sales_stats(self):
        """Get overall sales statistics"""
        if not self.data_loaded:
            raise ValueError("Data not loaded")
        
        return {
            'total_sales': float(self.df['total_sales'].sum()),
            'total_transactions': int(len(self.df)),
            'avg_transaction': float(self.df['total_sales'].mean()),
            'date_range': {
                'start': str(self.df['date'].min().date()),
                'end': str(self.df['date'].max().date())
            }
        }
    
    def get_product_stats(self):
        """Get product category statistics"""
        product_stats = self.df.groupby('product_category').agg({
            'total_sales': ['sum', 'mean', 'count']
        }).round(2)
        
        product_stats.columns = ['total_sales', 'avg_sales', 'num_transactions']
        product_stats = product_stats.sort_values('total_sales', ascending=False)
        
        result = []
        for product, row in product_stats.iterrows():
            result.append({
                'product': product,
                'total_sales': float(row['total_sales']),
                'avg_sales': float(row['avg_sales']),
                'num_transactions': int(row['num_transactions'])
            })
        
        return result
    
    def get_region_stats(self):
        """Get regional statistics"""
        region_stats = self.df.groupby('region').agg({
            'total_sales': ['sum', 'mean', 'count']
        }).round(2)
        
        region_stats.columns = ['total_sales', 'avg_sales', 'num_transactions']
        region_stats = region_stats.sort_values('total_sales', ascending=False)
        
        result = []
        for region, row in region_stats.iterrows():
            result.append({
                'region': region,
                'total_sales': float(row['total_sales']),
                'avg_sales': float(row['avg_sales']),
                'num_transactions': int(row['num_transactions'])
            })
        
        return result
    
    def get_trends(self, period='monthly'):
        """Get sales trends"""
        df_copy = self.df.copy()
        
        if period == 'daily':
            trends = df_copy.groupby('date')['total_sales'].sum()
        elif period == 'weekly':
            df_copy['week'] = df_copy['date'].dt.to_period('W')
            trends = df_copy.groupby('week')['total_sales'].sum()
        else:  # monthly
            df_copy['month'] = df_copy['date'].dt.to_period('M')
            trends = df_copy.groupby('month')['total_sales'].sum()
        
        return {
            'periods': [str(p) for p in trends.index],
            'sales': [float(s) for s in trends.values]
        }
    
    def get_categories(self):
        """Get list of product categories"""
        return sorted(self.df['product_category'].unique().tolist())
    
    def get_historical_data(self, start_date=None, end_date=None, category=None):
        """Get historical data with filters"""
        df_filtered = self.df.copy()
        
        if start_date:
            df_filtered = df_filtered[df_filtered['date'] >= pd.to_datetime(start_date)]
        if end_date:
            df_filtered = df_filtered[df_filtered['date'] <= pd.to_datetime(end_date)]
        if category:
            df_filtered = df_filtered[df_filtered['product_category'] == category]
        
        daily_sales = df_filtered.groupby('date')['total_sales'].sum().reset_index()
        
        return {
            'dates': daily_sales['date'].dt.strftime('%Y-%m-%d').tolist(),
            'sales': daily_sales['total_sales'].round(2).tolist()
        }
    
    def generate_insights(self):
        """Generate business insights"""
        insights = []
        
        # Growth trend
        monthly_sales = self.df.groupby(
            self.df['date'].dt.to_period('M')
        )['total_sales'].sum()
        growth_rate = monthly_sales.pct_change().mean() * 100
        
        if growth_rate > 5:
            insights.append({
                'category': 'Growth',
                'severity': 'positive',
                'title': 'Strong Growth Trend',
                'description': f'Average monthly growth of {growth_rate:.1f}%',
                'recommendation': 'Scale operations to meet increasing demand'
            })
        
        # Top product
        top_product = self.df.groupby('product_category')['total_sales'].sum().idxmax()
        insights.append({
            'category': 'Products',
            'severity': 'info',
            'title': f'{top_product} - Top Performer',
            'description': f'{top_product} generates highest revenue',
            'recommendation': f'Expand {top_product} product line'
        })
        
        # Top region
        top_region = self.df.groupby('region')['total_sales'].sum().idxmax()
        insights.append({
            'category': 'Geography',
            'severity': 'info',
            'title': f'{top_region} - Leading Market',
            'description': f'{top_region} shows strongest performance',
            'recommendation': f'Use {top_region} strategy as template'
        })
        
        return insights
