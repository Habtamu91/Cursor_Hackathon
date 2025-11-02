"""
Business Insight Engine
Generates actionable insights from sales data and forecasts
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class InsightEngine:
    """Generate business insights from sales data"""
    
    def __init__(self, sales_df, forecast_df=None):
        self.sales_df = sales_df.copy()
        self.forecast_df = forecast_df
        self.insights = []
        
    def analyze_trends(self):
        """Analyze sales trends"""
        print("Analyzing trends...")
        
        # Convert date column
        self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
        
        # Monthly aggregation
        monthly_sales = self.sales_df.groupby(
            self.sales_df['date'].dt.to_period('M')
        )['total_sales'].sum()
        
        # Calculate growth rates
        growth_rates = monthly_sales.pct_change() * 100
        avg_growth = growth_rates.mean()
        recent_growth = growth_rates.iloc[-3:].mean()
        
        # Trend insights
        if avg_growth > 5:
            self.insights.append({
                'category': 'Growth',
                'severity': 'positive',
                'title': 'Strong Overall Growth',
                'description': f'Average monthly growth rate is {avg_growth:.1f}%',
                'recommendation': 'Scale operations to meet increasing demand'
            })
        elif avg_growth < -5:
            self.insights.append({
                'category': 'Growth',
                'severity': 'warning',
                'title': 'Declining Sales Trend',
                'description': f'Average monthly decline of {abs(avg_growth):.1f}%',
                'recommendation': 'Review pricing, marketing, and product mix'
            })
        
        if recent_growth > avg_growth + 5:
            self.insights.append({
                'category': 'Growth',
                'severity': 'positive',
                'title': 'Accelerating Growth',
                'description': f'Recent growth ({recent_growth:.1f}%) exceeds average ({avg_growth:.1f}%)',
                'recommendation': 'Invest in inventory and marketing to capitalize on momentum'
            })
    
    def analyze_seasonality(self):
        """Analyze seasonal patterns"""
        print("Analyzing seasonality...")
        
        # Monthly average sales
        self.sales_df['month'] = pd.to_datetime(self.sales_df['date']).dt.month
        monthly_avg = self.sales_df.groupby('month')['total_sales'].mean()
        
        peak_months = monthly_avg.nlargest(3).index.tolist()
        low_months = monthly_avg.nsmallest(3).index.tolist()
        
        month_names = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        
        peak_names = [month_names[m] for m in peak_months]
        low_names = [month_names[m] for m in low_months]
        
        self.insights.append({
            'category': 'Seasonality',
            'severity': 'info',
            'title': 'Peak Sales Periods',
            'description': f'Highest sales occur in {", ".join(peak_names)}',
            'recommendation': f'Increase inventory and staffing during {", ".join(peak_names)}'
        })
        
        self.insights.append({
            'category': 'Seasonality',
            'severity': 'info',
            'title': 'Low Sales Periods',
            'description': f'Lowest sales occur in {", ".join(low_names)}',
            'recommendation': f'Run promotions and marketing campaigns during {", ".join(low_names)}'
        })
    
    def analyze_products(self):
        """Analyze product performance"""
        print("Analyzing products...")
        
        # Product category performance
        product_sales = self.sales_df.groupby('product_category').agg({
            'total_sales': ['sum', 'mean', 'count']
        }).round(2)
        
        product_sales.columns = ['total_sales', 'avg_transaction', 'num_transactions']
        product_sales = product_sales.sort_values('total_sales', ascending=False)
        
        # Top performers
        top_product = product_sales.index[0]
        top_revenue = product_sales.iloc[0]['total_sales']
        
        # Underperformers
        bottom_product = product_sales.index[-1]
        bottom_revenue = product_sales.iloc[-1]['total_sales']
        
        self.insights.append({
            'category': 'Products',
            'severity': 'positive',
            'title': f'{top_product} - Top Performer',
            'description': f'Generated ETB {top_revenue:,.2f} in total sales',
            'recommendation': f'Expand {top_product} product line and increase marketing investment'
        })
        
        revenue_ratio = top_revenue / bottom_revenue
        if revenue_ratio > 10:
            self.insights.append({
                'category': 'Products',
                'severity': 'warning',
                'title': f'{bottom_product} - Underperforming',
                'description': f'Only ETB {bottom_revenue:,.2f} in sales (vs ETB {top_revenue:,.2f} for top product)',
                'recommendation': f'Consider discontinuing or repositioning {bottom_product}'
            })
    
    def analyze_regions(self):
        """Analyze regional performance"""
        print("Analyzing regions...")
        
        # Regional sales
        regional_sales = self.sales_df.groupby('region').agg({
            'total_sales': ['sum', 'mean']
        }).round(2)
        
        regional_sales.columns = ['total_sales', 'avg_sales']
        regional_sales = regional_sales.sort_values('total_sales', ascending=False)
        
        # Top and bottom regions
        top_region = regional_sales.index[0]
        bottom_region = regional_sales.index[-1]
        
        self.insights.append({
            'category': 'Geography',
            'severity': 'positive',
            'title': f'{top_region} - Top Regional Market',
            'description': f'Leading region with ETB {regional_sales.loc[top_region, "total_sales"]:,.2f} in sales',
            'recommendation': f'Use {top_region} as model for other regions'
        })
        
        self.insights.append({
            'category': 'Geography',
            'severity': 'warning',
            'title': f'{bottom_region} - Growth Opportunity',
            'description': f'Underdeveloped market with only ETB {regional_sales.loc[bottom_region, "total_sales"]:,.2f}',
            'recommendation': f'Increase marketing and distribution efforts in {bottom_region}'
        })
    
    def analyze_customer_segments(self):
        """Analyze customer segment performance"""
        print("Analyzing customer segments...")
        
        segment_sales = self.sales_df.groupby('customer_segment').agg({
            'total_sales': ['sum', 'mean', 'count']
        }).round(2)
        
        segment_sales.columns = ['total_sales', 'avg_transaction', 'num_transactions']
        segment_sales = segment_sales.sort_values('total_sales', ascending=False)
        
        top_segment = segment_sales.index[0]
        
        self.insights.append({
            'category': 'Customers',
            'severity': 'info',
            'title': f'{top_segment} - Primary Customer Base',
            'description': f'{top_segment} generates most revenue with ETB {segment_sales.loc[top_segment, "total_sales"]:,.2f}',
            'recommendation': f'Develop loyalty programs and exclusive offers for {top_segment} customers'
        })
    
    def analyze_forecast(self):
        """Analyze forecast predictions"""
        if self.forecast_df is None:
            return
        
        print("Analyzing forecast...")
        
        # Get recent actual and future forecast
        recent_avg = self.sales_df.groupby('date')['total_sales'].sum().iloc[-30:].mean()
        forecast_avg = self.forecast_df.iloc[-30:]['yhat'].mean()
        
        change_pct = ((forecast_avg - recent_avg) / recent_avg) * 100
        
        if change_pct > 10:
            self.insights.append({
                'category': 'Forecast',
                'severity': 'positive',
                'title': 'Strong Growth Expected',
                'description': f'Forecasted sales {change_pct:.1f}% higher than current levels',
                'recommendation': 'Prepare for increased demand with inventory and staffing'
            })
        elif change_pct < -10:
            self.insights.append({
                'category': 'Forecast',
                'severity': 'warning',
                'title': 'Sales Decline Expected',
                'description': f'Forecasted sales {abs(change_pct):.1f}% lower than current levels',
                'recommendation': 'Implement promotional campaigns and review pricing strategy'
            })
        else:
            self.insights.append({
                'category': 'Forecast',
                'severity': 'info',
                'title': 'Stable Sales Expected',
                'description': f'Forecasted sales remain within ±10% of current levels',
                'recommendation': 'Maintain current operations and monitor for changes'
            })
    
    def generate_all_insights(self):
        """Generate all insights"""
        print("\n" + "="*60)
        print("GENERATING BUSINESS INSIGHTS")
        print("="*60 + "\n")
        
        self.analyze_trends()
        self.analyze_seasonality()
        self.analyze_products()
        self.analyze_regions()
        self.analyze_customer_segments()
        self.analyze_forecast()
        
        print(f"\n[OK] Generated {len(self.insights)} insights\n")
        
        return self.insights
    
    def display_insights(self):
        """Display insights in formatted output"""
        if not self.insights:
            self.generate_all_insights()
        
        print("\n" + "="*60)
        print("BUSINESS INSIGHTS & RECOMMENDATIONS")
        print("="*60 + "\n")
        
        for i, insight in enumerate(self.insights, 1):
            severity_icons = {
                'positive': '[+]',
                'warning': '[!]',
                'info': '[i]'
            }
            
            icon = severity_icons.get(insight['severity'], '[*]')
            
            print(f"{icon} {insight['title']}")
            print(f"   Category: {insight['category']}")
            print(f"   Finding: {insight['description']}")
            print(f"   Action: {insight['recommendation']}")
            print()
    
    def export_insights(self, output_path='reports/insights.csv'):
        """Export insights to CSV"""
        if not self.insights:
            self.generate_all_insights()
        
        df_insights = pd.DataFrame(self.insights)
        df_insights.to_csv(output_path, index=False)
        print(f"[OK] Insights exported to {output_path}")


def main():
    """Main function for testing"""
    # Load sales data
    print("Loading data...")
    sales_df = pd.read_csv('data/raw/ethiopia_sales_raw.csv')
    
    # Load forecast if available
    try:
        forecast_df = pd.read_csv('data/forecasts/forecast_results.csv')
    except:
        forecast_df = None
    
    # Generate insights
    engine = InsightEngine(sales_df, forecast_df)
    engine.generate_all_insights()
    engine.display_insights()
    
    # Export insights
    engine.export_insights('reports/insights.csv')


if __name__ == "__main__":
    main()

