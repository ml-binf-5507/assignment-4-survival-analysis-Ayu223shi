"""
cox_model.py

Students implement Cox Proportional Hazards regression.
"""

from typing import Any, Dict, List, Tuple
import pandas as pd
import numpy as np


def fit_cox_model(
    data: pd.DataFrame,
    time_col: str,
    event_col: str,
    covariates: List[str],
) -> Any:
    """Fit Cox Proportional Hazards model.

    Parameters
    ----------
    data : pd.DataFrame
        Survival dataset with time, event, and covariate columns.
    time_col : str
        Name of survival time column.
    event_col : str
        Name of event indicator column (1=event, 0=censored).
    covariates : list of str
        List of covariate column names to include in model.
        Must contain ≥3 covariates.

    Returns
    -------
    CoxPHFitter
        Fitted Cox model object.

    Example
    -------
    >>> covariates = ['age', 'stage', 'treatment', 'biomarker']
    >>> cox = fit_cox_model(data, 'time', 'event', covariates)
    """
    if len(covariates) < 3:
        raise ValueError("Cox model must include at least 3 covariates")
    
    raise NotImplementedError("Implement Cox PH model fitting here")


def extract_cox_summary(cox_model: Any) -> pd.DataFrame:
    """Extract summary statistics from fitted Cox model.

    Parameters
    ----------
    cox_model : CoxPHFitter
        Fitted Cox model.

    Returns
    -------
    pd.DataFrame
        Summary table with columns:
        - covariate: variable name
        - coef: regression coefficient
        - exp(coef): hazard ratio
        - se(coef): standard error
        - z: z-score
        - p: p-value
        - lower 95%: lower CI bound for HR
        - upper 95%: upper CI bound for HR

    Example
    -------
    >>> summary = extract_cox_summary(cox)
    >>> summary.to_csv('outputs/cox_summary.csv', index=False)
    """
    raise NotImplementedError("Implement Cox summary extraction here")


def test_proportional_hazards(
    cox_model: Any,
    data: pd.DataFrame,
    time_col: str,
    event_col: str,
) -> Dict[str, Dict[str, float]]:
    """Test proportional hazards assumption using Schoenfeld residuals.

    Parameters
    ----------
    cox_model : CoxPHFitter
        Fitted Cox model.
    data : pd.DataFrame
        Training data used to fit the model.
    time_col : str
        Name of time column.
    event_col : str
        Name of event column.

    Returns
    -------
    dict
        Nested dictionary with test results for each covariate.
        Format: {
            'covariate1': {'test_statistic': float, 'p_value': float},
            'covariate2': {'test_statistic': float, 'p_value': float},
            ...
        }

    Notes
    -----
    - p-value > 0.05: PH assumption satisfied for that covariate
    - p-value < 0.05: PH assumption may be violated
    
    Example
    -------
    >>> ph_test = test_proportional_hazards(cox, data, 'time', 'event')
    >>> # ph_test = {
    >>> #     'age': {'test_statistic': 0.85, 'p_value': 0.356},
    >>> #     'stage': {'test_statistic': 2.41, 'p_value': 0.120}
    >>> # }
    """
    raise NotImplementedError("Implement PH assumption test here")
