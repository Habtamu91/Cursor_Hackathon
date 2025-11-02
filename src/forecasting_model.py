"""
Sales Forecasting Model using Prophet and statistical methods
"""

import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


class SalesForecaster:
    """Sales forecasting using Prophet with multiple features"""
    
    def __init__(self):
        self.model = None
        self.df_train = None
        self.df_test = None
        
    def prepare_data(self, df, date_col='date', value_col='total_sales', 
                     test_size=90):
        """
        Prepare data for Prophet model
        
        Args:
            df: DataFrame with sales data
            date_col: Name of date column
            value_col: Name of sales value column
            test_size: Number of days for test set
        """
        # Aggregate daily sales
        df_daily = df.groupby(date_col)[value_col].sum().reset_index()
        df_daily.columns = ['ds', 'y']
        
        # Split train/test
        split_idx = len(df_daily) - test_size
        self.df_train = df_daily.iloc[:split_idx].copy()
        self.df_test = df_daily.iloc[split_idx:].copy()
        
        print(f"Training data: {len(self.df_train)} days")
        print(f"Test data: {len(self.df_test)} days")
        
        return self.df_train, self.df_test
    
    def train_model(self, yearly_seasonality=True, weekly_seasonality=True,
                   daily_seasonality=False, changepoint_prior_scale=0.05):
        """
        Train Prophet forecasting model
        
        Args:
            yearly_seasonality: Include yearly patterns
            weekly_seasonality: Include weekly patterns
            daily_seasonality: Include daily patterns
            changepoint_prior_scale: Model flexibility
        """
        print("Training forecasting model...")
        
        self.model = Prophet(
            yearly_seasonality=yearly_seasonality,
            weekly_seasonality=weekly_seasonality,
            daily_seasonality=daily_seasonality,
            changepoint_prior_scale=changepoint_prior_scale,
            seasonality_mode='multiplicative'
        )
        
        # Add custom seasonality for Ethiopian calendar
        self.model.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        )
        
        self.model.fit(self.df_train)
        print("Model training completed!")
        
    def forecast(self, periods=90):
        """
        Generate forecast for future periods
        
        Args:
            periods: Number of days to forecast
            
        Returns:
            DataFrame with forecast results
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train_model() first.")
        
        # Create future dataframe
        future = self.model.make_future_dataframe(periods=periods)
        
        # Generate forecast
        forecast = self.model.predict(future)
        
        return forecast
    
    def evaluate_model(self):
        """
        Evaluate model performance on test set
        
        Returns:
            Dictionary with evaluation metrics
        """
        # Forecast on test period
        future = self.df_train.copy()
        future = pd.concat([future, self.df_test[['ds']]], ignore_index=True)
        forecast = self.model.predict(future)
        
        # Get predictions for test period
        test_forecast = forecast.iloc[-len(self.df_test):].copy()
        y_true = self.df_test['y'].values
        y_pred = test_forecast['yhat'].values
        
        # Calculate metrics
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        r2 = r2_score(y_true, y_pred)
        
        metrics = {
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape,
            'R2': r2
        }
        
        print("\n" + "="*50)
        print("MODEL EVALUATION METRICS")
        print("="*50)
        print(f"Mean Absolute Error (MAE): ETB {mae:,.2f}")
        print(f"Root Mean Squared Error (RMSE): ETB {rmse:,.2f}")
        print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
        print(f"R² Score: {r2:.4f}")
        print("="*50 + "\n")
        
        return metrics
    
    def get_forecast_summary(self, forecast_df):
        """
        Get summary statistics for forecast
        
        Args:
            forecast_df: DataFrame from forecast()
            
        Returns:
            Dictionary with summary statistics
        """
        future_forecast = forecast_df.iloc[-90:].copy()  # Last 90 days
        
        summary = {
            'total_forecasted_sales': future_forecast['yhat'].sum(),
            'avg_daily_sales': future_forecast['yhat'].mean(),
            'min_daily_sales': future_forecast['yhat'].min(),
            'max_daily_sales': future_forecast['yhat'].max(),
            'trend': 'increasing' if future_forecast['yhat'].iloc[-1] > future_forecast['yhat'].iloc[0] else 'decreasing'
        }
        
        return summary


class CategoryForecaster:
    """Forecast sales by category"""
    
    def __init__(self, df, category_col='product_category'):
        self.df = df
        self.category_col = category_col
        self.models = {}
        self.forecasts = {}
        
    def train_all_categories(self, test_size=90):
        """Train models for all categories"""
        categories = self.df[self.category_col].unique()
        
        print(f"\nTraining models for {len(categories)} categories...")
        
        for category in categories:
            print(f"\n--- {category} ---")
            
            # Filter data for category
            df_cat = self.df[self.df[self.category_col] == category].copy()
            
            # Initialize and train model
            forecaster = SalesForecaster()
            forecaster.prepare_data(df_cat, test_size=test_size)
            forecaster.train_model()
            
            # Store model
            self.models[category] = forecaster
            
        print("\n✓ All category models trained!")
        
    def forecast_all_categories(self, periods=90):
        """Generate forecasts for all categories"""
        print(f"\nGenerating {periods}-day forecasts for all categories...")
        
        for category, forecaster in self.models.items():
            forecast = forecaster.forecast(periods=periods)
            self.forecasts[category] = forecast
            
        print("✓ All forecasts generated!")
        
        return self.forecasts
    
    def get_combined_forecast(self):
        """Combine all category forecasts"""
        combined = pd.DataFrame()
        
        for category, forecast in self.forecasts.items():
            df_cat = forecast[['ds', 'yhat']].copy()
            df_cat['category'] = category
            combined = pd.concat([combined, df_cat], ignore_index=True)
            
        return combined


def main():
    """Main function for testing"""
    # Load data
    print("Loading sales data...")
    df = pd.read_csv('data/raw/ethiopia_sales_raw.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    # Overall forecast
    print("\n" + "="*60)
    print("OVERALL SALES FORECASTING")
    print("="*60)
    
    forecaster = SalesForecaster()
    forecaster.prepare_data(df, test_size=90)
    forecaster.train_model()
    
    # Evaluate
    metrics = forecaster.evaluate_model()
    
    # Generate forecast
    forecast = forecaster.forecast(periods=90)
    summary = forecaster.get_forecast_summary(forecast)
    
    print("\nFORECAST SUMMARY (Next 90 Days)")
    print("="*60)
    print(f"Total Forecasted Sales: ETB {summary['total_forecasted_sales']:,.2f}")
    print(f"Average Daily Sales: ETB {summary['avg_daily_sales']:,.2f}")
    print(f"Expected Range: ETB {summary['min_daily_sales']:,.2f} - ETB {summary['max_daily_sales']:,.2f}")
    print(f"Trend: {summary['trend'].upper()}")
    print("="*60)
    
    # Save forecast
    forecast.to_csv('data/forecasts/forecast_results.csv', index=False)
    print("\n[OK] Forecast saved to data/forecasts/forecast_results.csv")


if __name__ == "__main__":
    main()

