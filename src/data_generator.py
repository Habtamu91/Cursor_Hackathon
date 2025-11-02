"""
Data Generator for Ethiopia Sales Data
Generates synthetic sales data for business forecasting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class EthiopiaSalesDataGenerator:
    """Generate synthetic sales data for Ethiopian business context"""
    
    def __init__(self, start_date='2020-01-01', end_date='2024-10-31', seed=42):
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        
        # Ethiopian context
        self.regions = ['Addis Ababa', 'Oromia', 'Amhara', 'Tigray', 'SNNPR', 'Somali', 'Afar', 'Dire Dawa']
        self.product_categories = ['Coffee', 'Teff', 'Electronics', 'Textiles', 'Spices', 
                                  'Livestock', 'Vegetables', 'Injera', 'Leather Goods', 'Cereals']
        self.customer_segments = ['Retail', 'Wholesale', 'Export', 'B2B', 'Direct Consumer']
        
    def generate_date_range(self):
        """Generate daily date range"""
        return pd.date_range(start=self.start_date, end=self.end_date, freq='D')
    
    def add_seasonality(self, base_value, date):
        """Add seasonal patterns based on Ethiopian calendar and holidays"""
        # Monthly seasonality
        month_factor = 1 + 0.2 * np.sin(2 * np.pi * date.month / 12)
        
        # Ethiopian holidays boost (approximate Gregorian dates)
        if date.month == 9 and 1 <= date.day <= 15:  # Ethiopian New Year
            month_factor *= 1.5
        elif date.month == 1 and 7 <= date.day <= 20:  # Timkat
            month_factor *= 1.4
        elif date.month == 9 and 27 <= date.day <= 30:  # Meskel
            month_factor *= 1.3
        elif date.month == 12:  # Christmas season
            month_factor *= 1.6
            
        # Weekly pattern (weekend slightly lower)
        if date.dayofweek >= 5:  # Saturday, Sunday
            month_factor *= 0.85
            
        return base_value * month_factor
    
    def add_trend(self, base_value, days_from_start):
        """Add growth trend"""
        # Annual growth rate of 8-12%
        annual_growth = 0.10
        daily_growth = annual_growth / 365
        return base_value * (1 + daily_growth * days_from_start)
    
    def add_noise(self, value):
        """Add random noise"""
        noise_factor = np.random.normal(1, 0.15)
        return value * noise_factor
    
    def generate_sales_data(self):
        """Generate complete sales dataset"""
        dates = self.generate_date_range()
        data = []
        
        transaction_id = 1000
        
        for date in dates:
            days_from_start = (date - self.start_date).days
            
            # Generate 5-20 transactions per day
            num_transactions = random.randint(5, 20)
            
            for _ in range(num_transactions):
                region = random.choice(self.regions)
                product = random.choice(self.product_categories)
                segment = random.choice(self.customer_segments)
                
                # Base sales amount varies by product
                base_amounts = {
                    'Coffee': 5000, 'Teff': 3000, 'Electronics': 15000,
                    'Textiles': 8000, 'Spices': 2000, 'Livestock': 20000,
                    'Vegetables': 1500, 'Injera': 1000, 'Leather Goods': 12000,
                    'Cereals': 4000
                }
                
                base_amount = base_amounts.get(product, 5000)
                
                # Apply transformations
                amount = self.add_trend(base_amount, days_from_start)
                amount = self.add_seasonality(amount, date)
                amount = self.add_noise(amount)
                amount = max(100, amount)  # Minimum transaction
                
                # Quantity based on amount and average unit price
                unit_price = base_amount / 10
                quantity = int(amount / unit_price)
                quantity = max(1, quantity)
                
                # Regional adjustment
                if region == 'Addis Ababa':
                    amount *= 1.3
                elif region == 'Oromia':
                    amount *= 1.1
                elif region == 'Afar':
                    amount *= 0.7
                    
                # Segment adjustment
                if segment == 'Wholesale':
                    amount *= 1.5
                    quantity *= 2
                elif segment == 'Export':
                    amount *= 2.0
                    quantity *= 3
                    
                data.append({
                    'transaction_id': transaction_id,
                    'date': date,
                    'region': region,
                    'product_category': product,
                    'customer_segment': segment,
                    'quantity': quantity,
                    'unit_price': round(amount / quantity, 2),
                    'total_sales': round(amount, 2),
                    'currency': 'ETB'
                })
                
                transaction_id += 1
        
        df = pd.DataFrame(data)
        return df
    
    def save_data(self, output_path='data/raw/ethiopia_sales_raw.csv'):
        """Generate and save sales data"""
        import os
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        print("Generating Ethiopia sales data...")
        df = self.generate_sales_data()
        df.to_csv(output_path, index=False)
        print(f"Generated {len(df)} transactions")
        print(f"Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"Data saved to {output_path}")
        return df


def main():
    """Main function to generate data"""
    generator = EthiopiaSalesDataGenerator(
        start_date='2020-01-01',
        end_date='2024-10-31',
        seed=42
    )
    
    df = generator.save_data()
    
    # Display summary statistics
    print("\n" + "="*60)
    print("DATA GENERATION SUMMARY")
    print("="*60)
    print(f"\nTotal Transactions: {len(df):,}")
    print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
    print(f"Total Sales: ETB {df['total_sales'].sum():,.2f}")
    print(f"Average Transaction: ETB {df['total_sales'].mean():,.2f}")
    print(f"\nRegions: {', '.join(df['region'].unique())}")
    print(f"Product Categories: {', '.join(df['product_category'].unique())}")
    print(f"Customer Segments: {', '.join(df['customer_segment'].unique())}")
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

