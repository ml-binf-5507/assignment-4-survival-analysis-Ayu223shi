"""
random_survival_forest.py

Students implement Random Survival Forest using scikit-survival.
"""

from typing import Any, Dict, List, Tuple
import pandas as pd
import numpy as np


def fit_random_survival_forest(
    X_train: pd.DataFrame,
    y_train: np.ndarray,
    n_estimators: int = 100,
    random_state: int = 42,
) -> Any:
    """Train a Random Survival Forest model.

    Parameters
    ----------
    X_train : pd.DataFrame
        Feature matrix (covariates) for training.
    y_train : np.ndarray
        Structured array with dtype=[('event', bool), ('time', float)].
        This is the scikit-survival format for survival outcomes.
    n_estimators : int
        Number of trees in the forest.
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    RandomSurvivalForest
        Fitted RSF model.

    Example
    -------
    >>> from sksurv.util import Surv
    >>> y_train = Surv.from_dataframe('event', 'time', data_train)
    >>> rsf = fit_random_survival_forest(X_train, y_train)
    """
    raise NotImplementedError("Implement Random Survival Forest fitting here")


def compute_concordance_index(
    rsf_model: Any,
    X_test: pd.DataFrame,
    y_test: np.ndarray,
) -> float:
    """Compute concordance index (C-index) for RSF predictions.

    Parameters
    ----------
    rsf_model : RandomSurvivalForest
        Fitted RSF model.
    X_test : pd.DataFrame
        Test feature matrix.
    y_test : np.ndarray
        Test survival outcomes in structured array format.

    Returns
    -------
    float
        Concordance index (Harrell's C-index).
        Range: [0, 1], where 0.5 = random, 1.0 = perfect.

    Example
    -------
    >>> c_index = compute_concordance_index(rsf, X_test, y_test)
    >>> print(f"C-index: {c_index:.3f}")
    """
    raise NotImplementedError("Implement C-index computation here")


def get_feature_importance(
    rsf_model: Any,
    feature_names: List[str],
) -> pd.DataFrame:
    """Extract feature importance scores from RSF model.

    Parameters
    ----------
    rsf_model : RandomSurvivalForest
        Fitted RSF model.
    feature_names : list of str
        Names of features (column names from X_train).

    Returns
    -------
    pd.DataFrame
        DataFrame with columns ['feature', 'importance'],
        sorted by importance in descending order.

    Example
    -------
    >>> importance = get_feature_importance(rsf, X_train.columns.tolist())
    >>> print(importance.head())
    """
    raise NotImplementedError("Implement feature importance extraction here")


def plot_feature_importance(
    importance_df: pd.DataFrame,
    filename: str = "rsf_importance.png",
    top_n: int = 10,
) -> None:
    """Create horizontal bar chart of feature importance.

    Parameters
    ----------
    importance_df : pd.DataFrame
        Output from get_feature_importance().
    filename : str
        Output filename for plot.
    top_n : int
        Number of top features to display.

    Notes
    -----
    Plot should include:
    - Horizontal bars showing importance scores
    - Feature names on y-axis
    - Sorted by importance (most important at top)
    - Clear title and axis labels
    """
    raise NotImplementedError("Implement importance plotting here")
