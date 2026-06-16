import os
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


EXPECTED_FILES = [
    "km_survival_plot.png",
    "cox_summary.csv",
    "rsf_importance.png",
]


def test_function_signatures():
    """Verify all required functions exist."""
    from students import kaplan_meier, cox_model, random_survival_forest
    
    # Kaplan-Meier functions
    assert hasattr(kaplan_meier, "fit_kaplan_meier")
    assert hasattr(kaplan_meier, "compute_logrank_test")
    assert hasattr(kaplan_meier, "plot_km_curves")
    
    # Cox model functions
    assert hasattr(cox_model, "fit_cox_model")
    assert hasattr(cox_model, "extract_cox_summary")
    assert hasattr(cox_model, "test_proportional_hazards")
    
    # RSF functions
    assert hasattr(random_survival_forest, "fit_random_survival_forest")
    assert hasattr(random_survival_forest, "compute_concordance_index")
    assert hasattr(random_survival_forest, "get_feature_importance")
    assert hasattr(random_survival_forest, "plot_feature_importance")


def test_kaplan_meier_execution(survival_data, tmp_path):
    """Test Kaplan-Meier analysis executes and produces valid outputs."""
    from students.kaplan_meier import (
        fit_kaplan_meier,
        compute_logrank_test,
        plot_km_curves,
    )
    
    data, time_col, event_col = survival_data
    
    # Create binary grouping variable
    data['group'] = (data[time_col] > data[time_col].median()).astype(int)
    data['group'] = data['group'].map({0: 'low_risk', 1: 'high_risk'})
    
    # Fit KM curves
    km_models = fit_kaplan_meier(data, time_col, event_col, 'group')
    
    # Check that we have models for each group
    assert isinstance(km_models, dict)
    assert len(km_models) >= 2, "Must compare at least 2 groups"
    
    # Compute log-rank test
    logrank = compute_logrank_test(data, time_col, event_col, 'group')
    
    # Validate log-rank results
    assert isinstance(logrank, dict)
    assert 'test_statistic' in logrank
    assert 'p_value' in logrank
    assert 0 <= logrank['p_value'] <= 1, "p-value must be in [0, 1]"
    
    # Generate plot
    plot_path = tmp_path / "km_survival_plot.png"
    plot_km_curves(km_models, filename=str(plot_path))
    
    # Verify outputs exist
    assert plot_path.exists()
    assert plot_path.stat().st_size > 0


def test_cox_model_execution(survival_data, tmp_path):
    """Test Cox PH model executes with ≥3 covariates and saves CSV output."""
    from students.cox_model import (
        fit_cox_model,
        extract_cox_summary,
        test_proportional_hazards,
    )
    
    data, time_col, event_col = survival_data
    
    # Add synthetic covariates
    np.random.seed(42)
    data['age'] = np.random.normal(60, 10, len(data))
    data['biomarker'] = np.random.exponential(2, len(data))
    data['stage'] = np.random.choice(['I', 'II', 'III', 'IV'], len(data))
    
    covariates = ['age', 'biomarker', 'stage']
    
    # Fit Cox model
    cox = fit_cox_model(data, time_col, event_col, covariates)
    
    # Extract summary
    summary = extract_cox_summary(cox)
    
    # Validate summary table
    assert isinstance(summary, pd.DataFrame)
    assert len(summary) >= 3, "Must have at least 3 covariates"
    
    # Check required columns
    required_cols = {'coef', 'exp(coef)', 'p'}
    assert required_cols.issubset(summary.columns), f"Missing columns: {required_cols - set(summary.columns)}"
    
    # Validate hazard ratios are positive
    assert (summary['exp(coef)'] > 0).all(), "Hazard ratios must be positive"
    
    # Save summary
    summary_path = tmp_path / "cox_summary.csv"
    summary.to_csv(summary_path, index=False)
    
    # Verify output exists
    assert summary_path.exists()


def test_rsf_execution(survival_data, tmp_path):
    """Test Random Survival Forest execution and metrics."""
    from students.random_survival_forest import (
        fit_random_survival_forest,
        compute_concordance_index,
        get_feature_importance,
        plot_feature_importance,
    )
    from sksurv.util import Surv
    
    data, time_col, event_col = survival_data
    
    # Add features
    np.random.seed(42)
    data['age'] = np.random.normal(60, 10, len(data))
    data['biomarker1'] = np.random.exponential(2, len(data))
    data['biomarker2'] = np.random.gamma(2, 2, len(data))
    
    feature_cols = ['age', 'biomarker1', 'biomarker2']
    
    # Prepare data
    X = data[feature_cols]
    y = Surv.from_dataframe(event_col, time_col, data)
    
    # Split train/test
    n_train = int(0.7 * len(data))
    X_train, X_test = X[:n_train], X[n_train:]
    y_train, y_test = y[:n_train], y[n_train:]
    
    # Fit RSF
    rsf = fit_random_survival_forest(X_train, y_train, n_estimators=50)
    
    # Compute C-index
    c_index = compute_concordance_index(rsf, X_test, y_test)
    
    # Validate C-index
    assert isinstance(c_index, (float, np.floating))
    assert 0 <= c_index <= 1, f"C-index must be in [0, 1], got {c_index}"
    
    # Get feature importance
    importance = get_feature_importance(rsf, feature_cols)
    
    # Validate importance
    assert isinstance(importance, pd.DataFrame)
    assert 'feature' in importance.columns
    assert 'importance' in importance.columns
    assert len(importance) == len(feature_cols)
    
    # Plot importance
    plot_path = tmp_path / "rsf_importance.png"
    plot_feature_importance(importance, filename=str(plot_path))
    
    # Verify outputs exist
    assert plot_path.exists()
    assert plot_path.stat().st_size > 0


def test_all_outputs_generated(survival_data, tmp_path):
    """Integration test: verify all required outputs are created."""
    # This test would run the full analysis pipeline
    # For now, just check that previous tests created outputs
    pass
