"""
Streamlit Dashboard for BizPredict
Interactive visualization and forecasting interface
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_generator import EthiopiaSalesDataGenerator
from forecasting_model import SalesForecaster
from insight_engine import InsightEngine


# Page configuration
st.set_page_config(
    page_title="BizPredict - Ethiopia Sales Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Narrow sidebar */
    [data-testid="stSidebar"] {
        min-width: 200px;
        max-width: 250px;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 250px;
    }
    
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-positive {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .insight-warning {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .insight-info {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin-bottom: 1rem;
    }
    
    /* Compact sidebar text */
    [data-testid="stSidebar"] h3 {
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 0.9rem;
    }
    
    /* Beautiful File Uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border: 2px dashed #667eea;
        border-radius: 12px;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2;
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    [data-testid="stFileUploader"] section {
        border: none !important;
        background: transparent !important;
    }
    [data-testid="stFileUploader"] button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* File uploader text */
    [data-testid="stFileUploader"] label {
        color: #667eea !important;
        font-weight: 600;
        font-size: 0.95rem;
    }
    [data-testid="stFileUploader"] small {
        color: #6c757d;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load sales data"""
    import os
    # Get project root directory (parent of dashboard)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, 'data', 'raw', 'ethiopia_sales_raw.csv')
    
    try:
        df = pd.read_csv(data_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.warning("Sales data not found. Generating sample data...")
        # Change to project root for data generation
        original_dir = os.getcwd()
        os.chdir(project_root)
        try:
            generator = EthiopiaSalesDataGenerator()
            df = generator.save_data()
            return df
        finally:
            os.chdir(original_dir)


@st.cache_resource
def train_forecaster(df):
    """Train forecasting model"""
    forecaster = SalesForecaster()
    forecaster.prepare_data(df, test_size=90)
    forecaster.train_model()
    return forecaster


def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 BizPredict</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Smart Business Forecasting for Ethiopia</p>', unsafe_allow_html=True)
    
    # Beautiful Sidebar
    with st.sidebar:
        # Beautiful Upload Section
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; 
                    border-radius: 10px; 
                    text-align: center;
                    margin-bottom: 1rem;'>
            <h3 style='color: white; margin: 0; font-size: 1.1rem;'>
                📊 Data Source
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload your sales data",
            type=['csv'],
            help="Drag & drop or click to browse",
            key="file_uploader"
        )
        
        # Load data with beautiful status
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                df['date'] = pd.to_datetime(df['date'])
                
                # Beautiful success message
                st.markdown(f"""
                <div style='background-color: #d4edda; 
                            padding: 0.75rem; 
                            border-radius: 8px; 
                            border-left: 4px solid #28a745;
                            margin: 0.5rem 0;'>
                    <p style='margin: 0; color: #155724; font-weight: 500;'>
                        ✓ Loaded: <strong>{len(df):,}</strong> records
                    </p>
                    <p style='margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #155724;'>
                        📁 {uploaded_file.name}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div style='background-color: #f8d7da; 
                            padding: 0.75rem; 
                            border-radius: 8px; 
                            border-left: 4px solid #dc3545;
                            margin: 0.5rem 0;'>
                    <p style='margin: 0; color: #721c24; font-weight: 500;'>
                        ⚠️ Error loading file
                    </p>
                    <p style='margin: 0.25rem 0 0 0; font-size: 0.85rem; color: #721c24;'>
                        {str(e)[:50]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
                with st.spinner('Loading default data...'):
                    df = load_data()
        else:
            with st.spinner('Loading...'):
                df = load_data()
            
            # Info about default data
            st.markdown("""
            <div style='background-color: #e7f3ff; 
                        padding: 0.6rem; 
                        border-radius: 8px; 
                        border-left: 4px solid #2196F3;
                        margin: 0.5rem 0;'>
                <p style='margin: 0; color: #014361; font-size: 0.85rem;'>
                    💡 Using default dataset<br>
                    <span style='font-size: 0.8rem;'>Upload CSV to analyze your data</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Compact Filters with Expander
        with st.expander("🎛️ Filters", expanded=True):
            date_range = st.date_input(
                "📅 Date",
                value=(df['date'].min(), df['date'].max()),
                label_visibility="visible"
            )
            
            selected_regions = st.multiselect(
                "🗺️ Region",
                options=sorted(df['region'].unique()),
                default=sorted(df['region'].unique())
            )
            
            selected_categories = st.multiselect(
                "🛍️ Products",
                options=sorted(df['product_category'].unique()),
                default=sorted(df['product_category'].unique())
            )
        
        # Filter data
        df_filtered = df[
            (df['date'] >= pd.to_datetime(date_range[0])) &
            (df['date'] <= pd.to_datetime(date_range[1])) &
            (df['region'].isin(selected_regions)) &
            (df['product_category'].isin(selected_categories))
        ]
        
        st.caption(f"📊 {len(df_filtered):,} / {len(df):,} records")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Overview", 
        "🔮 Forecasting", 
        "💡 Insights", 
        "📊 Analysis", 
        "🗺️ Regional View"
    ])
    
    with tab1:
        show_overview(df_filtered)
    
    with tab2:
        show_forecasting(df)
    
    with tab3:
        show_insights(df)
    
    with tab4:
        show_analysis(df_filtered)
    
    with tab5:
        show_regional_view(df_filtered)


def show_overview(df):
    """Overview page with key metrics"""
    st.header("Business Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sales = df['total_sales'].sum()
        st.metric("Total Sales", f"ETB {total_sales:,.0f}")
    
    with col2:
        total_transactions = len(df)
        st.metric("Transactions", f"{total_transactions:,}")
    
    with col3:
        avg_transaction = df['total_sales'].mean()
        st.metric("Avg Transaction", f"ETB {avg_transaction:,.2f}")
    
    with col4:
        num_days = (df['date'].max() - df['date'].min()).days + 1
        st.metric("Days of Data", f"{num_days:,}")
    
    st.markdown("---")
    
    # Sales trend
    st.subheader("📈 Sales Trend Over Time")
    daily_sales = df.groupby('date')['total_sales'].sum().reset_index()
    
    fig = px.line(
        daily_sales,
        x='date',
        y='total_sales',
        title='Daily Sales Performance',
        labels={'date': 'Date', 'total_sales': 'Total Sales (ETB)'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Product performance
        st.subheader("🛍️ Sales by Product Category")
        product_sales = df.groupby('product_category')['total_sales'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=product_sales.values,
            y=product_sales.index,
            orientation='h',
            labels={'x': 'Total Sales (ETB)', 'y': 'Product Category'},
            color=product_sales.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional performance
        st.subheader("🗺️ Sales by Region")
        region_sales = df.groupby('region')['total_sales'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=region_sales.values,
            y=region_sales.index,
            orientation='h',
            labels={'x': 'Total Sales (ETB)', 'y': 'Region'},
            color=region_sales.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)


def show_forecasting(df):
    """Forecasting page"""
    st.header("🔮 Sales Forecasting")
    
    # Forecast settings
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generate Forecast")
    
    with col2:
        forecast_days = st.selectbox("Forecast Period", [30, 60, 90, 180], index=2)
    
    if st.button("Generate Forecast", type="primary"):
        with st.spinner('Training model and generating forecast...'):
            # Train model
            forecaster = train_forecaster(df)
            
            # Generate forecast
            forecast = forecaster.forecast(periods=forecast_days)
            
            # Evaluate model
            metrics = forecaster.evaluate_model()
            
            # Display metrics
            st.success("✓ Forecast generated successfully!")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("MAE", f"ETB {metrics['MAE']:,.0f}")
            with col2:
                st.metric("RMSE", f"ETB {metrics['RMSE']:,.0f}")
            with col3:
                st.metric("MAPE", f"{metrics['MAPE']:.2f}%")
            with col4:
                st.metric("R² Score", f"{metrics['R2']:.4f}")
            
            st.markdown("---")
            
            # Plot forecast
            st.subheader("📊 Forecast Visualization")
            
            # Prepare data for plotting
            historical = df.groupby('date')['total_sales'].sum().reset_index()
            historical.columns = ['ds', 'y']
            
            forecast_plot = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            
            fig = go.Figure()
            
            # Historical data
            fig.add_trace(go.Scatter(
                x=historical['ds'],
                y=historical['y'],
                name='Historical',
                line=dict(color='blue')
            ))
            
            # Forecast
            fig.add_trace(go.Scatter(
                x=forecast_plot['ds'],
                y=forecast_plot['yhat'],
                name='Forecast',
                line=dict(color='red', dash='dash')
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_plot['ds'],
                y=forecast_plot['yhat_upper'],
                fill=None,
                mode='lines',
                line=dict(color='rgba(255,0,0,0)'),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_plot['ds'],
                y=forecast_plot['yhat_lower'],
                fill='tonexty',
                mode='lines',
                line=dict(color='rgba(255,0,0,0)'),
                name='Confidence Interval'
            ))
            
            fig.update_layout(
                title=f'{forecast_days}-Day Sales Forecast',
                xaxis_title='Date',
                yaxis_title='Total Sales (ETB)',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Forecast summary
            st.subheader("📋 Forecast Summary")
            future_forecast = forecast.iloc[-forecast_days:]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Forecasted Sales", f"ETB {future_forecast['yhat'].sum():,.0f}")
            with col2:
                st.metric("Average Daily Sales", f"ETB {future_forecast['yhat'].mean():,.0f}")
            with col3:
                trend = "Increasing" if future_forecast['yhat'].iloc[-1] > future_forecast['yhat'].iloc[0] else "Decreasing"
                st.metric("Trend", trend)


def show_insights(df):
    """Insights page"""
    st.header("💡 Business Insights & Recommendations")
    
    # Generate insights
    with st.spinner('Analyzing data and generating insights...'):
        engine = InsightEngine(df)
        insights = engine.generate_all_insights()
    
    st.success(f"✓ Generated {len(insights)} insights")
    
    # Display insights by category
    categories = ['Growth', 'Seasonality', 'Products', 'Geography', 'Customers', 'Forecast']
    
    for category in categories:
        category_insights = [i for i in insights if i['category'] == category]
        
        if category_insights:
            st.subheader(f"{'📈' if category == 'Growth' else '🔄' if category == 'Seasonality' else '🛍️' if category == 'Products' else '🗺️' if category == 'Geography' else '👥' if category == 'Customers' else '🔮'} {category}")
            
            for insight in category_insights:
                severity_class = f"insight-{insight['severity']}"
                
                st.markdown(f"""
                <div class="{severity_class}">
                    <h4>{insight['title']}</h4>
                    <p><strong>Finding:</strong> {insight['description']}</p>
                    <p><strong>Recommendation:</strong> {insight['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)


def show_analysis(df):
    """Detailed analysis page"""
    st.header("📊 Detailed Analysis")
    
    # Time series decomposition
    st.subheader("📅 Monthly Sales Breakdown")
    
    monthly_sales = df.groupby(df['date'].dt.to_period('M'))['total_sales'].sum()
    monthly_df = pd.DataFrame({
        'Month': [str(m) for m in monthly_sales.index],
        'Sales': monthly_sales.values
    })
    
    fig = px.bar(
        monthly_df,
        x='Month',
        y='Sales',
        title='Monthly Sales Performance',
        labels={'Sales': 'Total Sales (ETB)'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Product analysis
    st.subheader("🛍️ Product Category Deep Dive")
    
    product_stats = df.groupby('product_category').agg({
        'total_sales': ['sum', 'mean', 'count']
    }).round(2)
    product_stats.columns = ['Total Sales', 'Avg Transaction', 'Num Transactions']
    product_stats = product_stats.sort_values('Total Sales', ascending=False)
    
    st.dataframe(product_stats, use_container_width=True)
    
    # Customer segment analysis
    st.subheader("👥 Customer Segment Analysis")
    
    segment_sales = df.groupby('customer_segment')['total_sales'].sum().sort_values(ascending=False)
    
    fig = px.pie(
        values=segment_sales.values,
        names=segment_sales.index,
        title='Sales Distribution by Customer Segment'
    )
    st.plotly_chart(fig, use_container_width=True)


def show_regional_view(df):
    """Regional analysis page"""
    st.header("🗺️ Regional Performance Analysis")
    
    # Regional metrics
    region_stats = df.groupby('region').agg({
        'total_sales': ['sum', 'mean', 'count']
    }).round(2)
    region_stats.columns = ['Total Sales', 'Avg Transaction', 'Num Transactions']
    region_stats = region_stats.sort_values('Total Sales', ascending=False)
    
    st.subheader("📊 Regional Statistics")
    st.dataframe(region_stats, use_container_width=True)
    
    # Regional comparison
    st.subheader("🏆 Regional Comparison")
    
    fig = px.bar(
        x=region_stats.index,
        y=region_stats['Total Sales'],
        title='Total Sales by Region',
        labels={'x': 'Region', 'y': 'Total Sales (ETB)'},
        color=region_stats['Total Sales'],
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional trends
    st.subheader("📈 Regional Sales Trends")
    
    monthly_regional = df.groupby([df['date'].dt.to_period('M'), 'region'])['total_sales'].sum().reset_index()
    monthly_regional['date'] = monthly_regional['date'].astype(str)
    
    fig = px.line(
        monthly_regional,
        x='date',
        y='total_sales',
        color='region',
        title='Monthly Sales by Region',
        labels={'date': 'Month', 'total_sales': 'Total Sales (ETB)', 'region': 'Region'}
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
