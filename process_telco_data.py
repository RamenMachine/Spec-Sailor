"""
Main orchestration script for Telco Customer Churn data processing
Runs the complete pipeline: load → clean → engineer features → train model
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data.data_loader import load_telco_data
from data.data_cleaner import clean_telco_data
from features.feature_engineering import engineer_all_features
from models.train_model import train_xgboost_model


def main():
    """Run the complete data processing and model training pipeline"""
    print("=" * 60)
    print("CHURNGUARD PRO - DATA PROCESSING PIPELINE")
    print("=" * 60)
    
    try:
        # Step 1: Load data
        print("\n[STEP 1/4] Loading Telco dataset...")
        df_raw = load_telco_data()
        print(f"✓ Loaded {len(df_raw)} customers")
        
        # Step 2: Clean data
        print("\n[STEP 2/4] Cleaning data...")
        df_clean = clean_telco_data(df_raw)
        print(f"✓ Cleaned data: {df_clean.shape}")
        
        # Step 3: Engineer features
        print("\n[STEP 3/4] Engineering features...")
        X, y = engineer_all_features(df_clean)
        print(f"✓ Engineered {X.shape[1]} features")
        
        # Step 4: Train model
        print("\n[STEP 4/4] Training XGBoost model...")
        model, scaler, metrics = train_xgboost_model()
        print(f"✓ Model trained with {metrics['accuracy']:.2%} accuracy")
        
        print("\n" + "=" * 60)
        print("PIPELINE COMPLETE!")
        print("=" * 60)
        print(f"\n[SUCCESS] All steps completed successfully!")
        print(f"  - Data loaded and cleaned: {df_clean.shape[0]} customers")
        print(f"  - Features engineered: {X.shape[1]} features")
        print(f"  - Model accuracy: {metrics['accuracy']:.2%}")
        print(f"  - ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"\n[INFO] Next steps:")
        print(f"  1. Start API: python api/simple_api.py")
        print(f"  2. Start frontend: npm run dev")
        print(f"  3. View dashboard at http://localhost:8080")
        
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

