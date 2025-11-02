"""
Setup script for BizPredict
"""

import os
import subprocess
import sys


def install_dependencies():
    """Install all required dependencies"""
    print("Installing dependencies...")
    
    packages = [
        "pandas",
        "numpy",
        "prophet",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "plotly",
        "fastapi",
        "uvicorn",
        "streamlit",
        "jupyter"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("\n✓ All dependencies installed!")


def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    directories = [
        "data/raw",
        "data/processed",
        "data/forecasts",
        "reports",
        "notebooks",
        "src",
        "backend",
        "dashboard"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ {directory}")
    
    print("\n✓ All directories created!")


def generate_data():
    """Generate sample sales data"""
    print("\nGenerating sample data...")
    
    try:
        from src.data_generator import EthiopiaSalesDataGenerator
        
        generator = EthiopiaSalesDataGenerator()
        df = generator.save_data()
        
        print(f"\n✓ Generated {len(df)} transactions!")
    except Exception as e:
        print(f"Error generating data: {e}")


def main():
    """Main setup function"""
    print("="*60)
    print("BizPredict Setup")
    print("="*60)
    
    choice = input("\nWhat would you like to do?\n"
                  "1. Install dependencies\n"
                  "2. Create directories\n"
                  "3. Generate sample data\n"
                  "4. Full setup (all of the above)\n"
                  "Choice (1-4): ")
    
    if choice == "1":
        install_dependencies()
    elif choice == "2":
        create_directories()
    elif choice == "3":
        generate_data()
    elif choice == "4":
        install_dependencies()
        create_directories()
        generate_data()
    else:
        print("Invalid choice!")
        return
    
    print("\n" + "="*60)
    print("✓ Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run 'python src/data_generator.py' to generate data")
    print("2. Run 'python src/forecasting_model.py' to train model")
    print("3. Run 'streamlit run dashboard/app.py' to start dashboard")
    print("="*60)


if __name__ == "__main__":
    main()

