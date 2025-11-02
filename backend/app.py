"""
FastAPI Backend for BizPredict
Serves forecasting models and business insights via REST API
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.model import ForecastingService

app = FastAPI(
    title="BizPredict API",
    description="Smart Business Forecasting API for Ethiopia Sales Data",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
forecast_service = ForecastingService()


# Pydantic models
class ForecastRequest(BaseModel):
    periods: int = 90
    category: Optional[str] = None
    region: Optional[str] = None


class ForecastResponse(BaseModel):
    dates: List[str]
    predictions: List[float]
    lower_bound: List[float]
    upper_bound: List[float]
    metrics: Dict


class SalesStats(BaseModel):
    total_sales: float
    total_transactions: int
    avg_transaction: float
    date_range: Dict[str, str]


class InsightItem(BaseModel):
    category: str
    severity: str
    title: str
    description: str
    recommendation: str


@app.on_event("startup")
async def startup_event():
    """Load data and train model on startup"""
    print("Loading sales data and training models...")
    forecast_service.load_data()
    forecast_service.train_model()
    print("✓ API ready!")


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to BizPredict API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "stats": "/api/stats",
            "forecast": "/api/forecast",
            "insights": "/api/insights",
            "products": "/api/products",
            "regions": "/api/regions"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "data_loaded": forecast_service.data_loaded,
        "model_trained": forecast_service.model_trained
    }


@app.get("/api/stats", response_model=SalesStats)
def get_sales_stats():
    """Get overall sales statistics"""
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    stats = forecast_service.get_sales_stats()
    return stats


@app.post("/api/forecast", response_model=ForecastResponse)
def get_forecast(request: ForecastRequest):
    """
    Generate sales forecast
    
    Args:
        request: ForecastRequest with periods, category, region filters
        
    Returns:
        Forecast predictions with confidence intervals
    """
    if not forecast_service.model_trained:
        raise HTTPException(status_code=503, detail="Model not trained")
    
    try:
        forecast = forecast_service.generate_forecast(
            periods=request.periods,
            category=request.category,
            region=request.region
        )
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/insights", response_model=List[InsightItem])
def get_insights():
    """Get business insights and recommendations"""
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    insights = forecast_service.generate_insights()
    return insights


@app.get("/api/products")
def get_product_stats():
    """Get product category statistics"""
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    product_stats = forecast_service.get_product_stats()
    return product_stats


@app.get("/api/regions")
def get_region_stats():
    """Get regional statistics"""
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    region_stats = forecast_service.get_region_stats()
    return region_stats


@app.get("/api/trends")
def get_trends(period: str = "monthly"):
    """
    Get sales trends
    
    Args:
        period: 'daily', 'weekly', or 'monthly'
    """
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    trends = forecast_service.get_trends(period)
    return trends


@app.get("/api/categories")
def get_categories():
    """Get list of available product categories"""
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return {
        "categories": forecast_service.get_categories()
    }


@app.get("/api/historical")
def get_historical_data(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    category: Optional[str] = None
):
    """Get historical sales data with optional filters"""
    if not forecast_service.data_loaded:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    data = forecast_service.get_historical_data(
        start_date=start_date,
        end_date=end_date,
        category=category
    )
    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
