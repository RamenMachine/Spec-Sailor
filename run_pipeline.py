"""
Complete Pipeline Runner
Runs the entire Barakah Retain pipeline from data generation to model training
"""

import subprocess
import sys
import os
from datetime import datetime

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} complete")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Run complete pipeline"""
    start_time = datetime.now()

    print_header("BARAKAH RETAIN - COMPLETE PIPELINE")

    steps = [
        # Step 1: Generate Data
        {
            'command': 'python src/data/data_generator.py',
            'description': 'Step 1: Generate synthetic data',
            'required': True
        },
        # Step 2: Engineer Features
        {
            'command': 'python src/features/quick_features.py',
            'description': 'Step 2: Engineer features',
            'required': True
        },
        # Step 3: Train Model
        {
            'command': 'python src/models/train_model.py',
            'description': 'Step 3: Train XGBoost model',
            'required': True
        },
        # Step 4: Generate SHAP Explanations
        {
            'command': 'python src/models/explain.py',
            'description': 'Step 4: Generate SHAP explanations',
            'required': False
        },
    ]

    completed = 0
    for step in steps:
        success = run_command(step['command'], step['description'])

        if success:
            completed += 1
        elif step['required']:
            print(f"\n✗ Pipeline failed at: {step['description']}")
            print("Fix the error and run again.")
            sys.exit(1)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print_header("PIPELINE COMPLETE")
    print(f"✓ Completed {completed}/{len(steps)} steps")
    print(f"⏱ Total time: {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print("\nNext steps:")
    print("  1. Start API: python api/main.py")
    print("  2. Start frontend: npm run dev")
    print("  3. Visit: http://localhost:5173")

if __name__ == "__main__":
    main()
