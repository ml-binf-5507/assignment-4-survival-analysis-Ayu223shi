import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


# Ensure repository root is on Python path so `students` is importable in CI/local runs.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture
def survival_data():
    """Generate synthetic survival data for testing.
    
    Returns
    -------
    tuple
        (data, time_col, event_col)
    """
    np.random.seed(42)
    n = 200
    
    # Generate synthetic survival times
    time = np.random.exponential(scale=100, size=n)
    
    # Generate censoring (some observations are censored)
    censoring_time = np.random.exponential(scale=120, size=n)
    observed_time = np.minimum(time, censoring_time)
    event = (time <= censoring_time).astype(int)
    
    # Create DataFrame
    data = pd.DataFrame({
        'time': observed_time,
        'event': event,
    })
    
    # Ensure positive times
    data = data[data['time'] > 0].reset_index(drop=True)
    
    return data, 'time', 'event'
