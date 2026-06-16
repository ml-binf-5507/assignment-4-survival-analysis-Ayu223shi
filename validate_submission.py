#!/usr/bin/env python3
"""
Local validation script for Assignment 4 - Survival Analysis

Run this before pushing to verify your submission is complete.
"""

import inspect
import sys
from pathlib import Path
import pandas as pd

# Required output files
REQUIRED_FILES = [
    "outputs/km_survival_plot.png",
    "outputs/cox_summary.csv",
    "outputs/rsf_importance.png",
]

# Required functions
REQUIRED_FUNCTIONS = [
    ("students.kaplan_meier", "fit_kaplan_meier"),
    ("students.kaplan_meier", "compute_logrank_test"),
    ("students.kaplan_meier", "plot_km_curves"),
    ("students.cox_model", "fit_cox_model"),
    ("students.cox_model", "extract_cox_summary"),
    ("students.cox_model", "test_proportional_hazards"),
    ("students.random_survival_forest", "fit_random_survival_forest"),
    ("students.random_survival_forest", "compute_concordance_index"),
    ("students.random_survival_forest", "get_feature_importance"),
    ("students.random_survival_forest", "plot_feature_importance"),
]


def check_files():
    """Check if all required output files exist."""
    print("Checking output files...")
    missing = []
    
    for filepath in REQUIRED_FILES:
        path = Path(filepath)
        if not path.exists():
            missing.append(filepath)
            print(f"  ❌ Missing: {filepath}")
        else:
            print(f"  ✅ Found: {filepath}")
    
    return len(missing) == 0


def check_functions():
    """Check if all required functions are implemented."""
    print("\nChecking function implementations...")
    missing = []
    unimplemented = []
    
    for module_name, func_name in REQUIRED_FUNCTIONS:
        try:
            module = __import__(module_name, fromlist=[func_name])
            func = getattr(module, func_name, None)
            
            if func is None:
                missing.append(f"{module_name}.{func_name}")
                print(f"  ❌ Missing: {module_name}.{func_name}")
            else:
                # Check if still raises NotImplementedError
                source = inspect.getsource(func)
                if 'NotImplementedError' in source:
                    unimplemented.append(f"{module_name}.{func_name}")
                    print(f"  ⚠️  Not implemented: {module_name}.{func_name}")
                else:
                    print(f"  ✅ Implemented: {module_name}.{func_name}")
        
        except Exception as e:
            print(f"  ❌ Error checking {module_name}.{func_name}: {e}")
            missing.append(f"{module_name}.{func_name}")
    
    return len(missing) == 0 and len(unimplemented) == 0


def validate_metrics():
    """Validate key values in Cox summary output."""
    print("\nValidating metrics...")
    valid = True
    
    try:
        summary = pd.read_csv("outputs/cox_summary.csv")
        required_cols = {"coef", "exp(coef)", "p"}
        missing_cols = required_cols - set(summary.columns)
        if missing_cols:
            print(f"  ❌ Missing Cox summary columns: {missing_cols}")
            valid = False
        else:
            print("  ✅ Cox summary columns found")

        if "exp(coef)" in summary.columns and not (summary["exp(coef)"] > 0).all():
            print("  ❌ Invalid hazard ratios: exp(coef) must be positive")
            valid = False
        else:
            print("  ✅ Hazard ratios are positive")
    except Exception as e:
        print(f"  ⚠️  Could not validate outputs/cox_summary.csv: {e}")
    
    print("  ℹ️  RSF C-index is validated by the pytest autograder.")
    
    return valid


def main():
    """Run all validation checks."""
    print("=" * 60)
    print("Assignment 4 - Survival Analysis Validation")
    print("=" * 60)
    
    files_ok = check_files()
    funcs_ok = check_functions()
    metrics_ok = validate_metrics()
    
    print("\n" + "=" * 60)
    if files_ok and funcs_ok and metrics_ok:
        print("✅ ALL CHECKS PASSED")
        print("You're ready to push to GitHub!")
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        if not files_ok:
            print("  - Generate all required output files")
        if not funcs_ok:
            print("  - Implement all required functions")
        if not metrics_ok:
            print("  - Fix invalid metric values")
        return 1


if __name__ == "__main__":
    sys.exit(main())
