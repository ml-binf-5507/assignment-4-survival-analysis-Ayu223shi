# Survival Analysis Quick Reference

## Key Concepts

### Censoring
- **Right-censored**: Patient still alive at study end
- Censored observations contribute partial information
- Cannot be ignored (would bias results)

### Kaplan-Meier Estimator
**Non-parametric survival curve**

$$S(t) = \prod_{i: t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

Where:
- $d_i$ = number of events at time $t_i$
- $n_i$ = number at risk at time $t_i$

**When to use:**
- Simple group comparisons
- No covariates
- Visualizing survival patterns

### Cox Proportional Hazards

**Semi-parametric regression model**

$$h(t|X) = h_0(t) \exp(\beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_p X_p)$$

**Hazard Ratio (HR):**
- HR = 1: No effect
- HR > 1: Increased risk (worse survival)
- HR < 1: Decreased risk (better survival)

**Example interpretations:**
- HR = 2.0 for treatment → 2× higher hazard (worse)
- HR = 0.5 for biomarker → 50% reduction in hazard (better)

**Proportional hazards assumption:**
- HR stays constant over time
- Test with Schoenfeld residuals (p > 0.05 = assumption satisfied)

**When to use:**
- Want interpretable hazard ratios
- Need to adjust for multiple covariates
- Assume proportional hazards

### Random Survival Forest

**Machine learning ensemble**

- Extension of random forest to survival data
- Handles non-linear relationships
- Automatic interaction detection
- No proportional hazards assumption needed

**Concordance Index (C-index):**
- Probability model correctly ranks patient pairs
- 0.5 = random guessing
- 1.0 = perfect predictions
- Typical clinical: 0.6–0.75

**When to use:**
- Complex, non-linear relationships
- Feature interactions important
- Prediction more important than interpretation

---

## Common Workflows

### Exploratory Analysis
```python
# 1. Check event distribution
data['event'].value_counts()

# 2. Compute censoring rate
(1 - data['event'].mean()) * 100

# 3. Visualize survival times
data['time'].hist(bins=50)

# 4. Check for missing data
data.isnull().sum()
```

### Comparing Groups
```python
# Create groups
data['risk_group'] = pd.qcut(data['age'], q=3, labels=['Low', 'Med', 'High'])

# Fit KM curves
km = fit_kaplan_meier(data, 'time', 'event', 'risk_group')

# Statistical test
logrank = compute_logrank_test(data, 'time', 'event', 'risk_group')
```

### Building Predictive Model
```python
# Select features
features = ['age', 'stage', 'biomarker1', 'biomarker2']

# Prepare survival outcome
from sksurv.util import Surv
y = Surv.from_dataframe('event', 'time', data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    data[features], y, test_size=0.3, random_state=42
)

# Fit model
rsf = fit_random_survival_forest(X_train, y_train)

# Evaluate
c_index = compute_concordance_index(rsf, X_test, y_test)
```

---

## Troubleshooting

### "Convergence failed" in Cox model
**Cause:** Perfect separation or collinearity

**Solutions:**
- Remove highly correlated features
- Combine rare categories
- Increase sample size
- Try Firth's penalized Cox model

### "PH assumption violated"
**Cause:** Hazard ratio changes over time

**Solutions:**
- Stratify by violating variable
- Add time-varying coefficients
- Use extended Cox model
- Try Random Survival Forest instead

### Low C-index
**Causes:**
- Weak predictors
- High censoring rate
- Complex non-linear relationships

**Solutions:**
- Feature engineering
- Try RSF for non-linearity
- Add interaction terms to Cox
- Accept that prediction is hard!

### Negative survival times
**Cause:** Data error or improper time calculation

**Solution:**
```python
# Remove negative times
data = data[data['time'] > 0]

# Or investigate source of error
data[data['time'] <= 0]
```

---

## Statistical Tests Interpretation

### Log-rank test
- **H₀**: No difference in survival between groups
- **p < 0.05**: Significant difference (reject H₀)
- **p ≥ 0.05**: No significant difference

### Cox model coefficients
- **p < 0.05**: Significant predictor
- **β > 0**: Increases hazard (worse survival)
- **β < 0**: Decreases hazard (better survival)

### Schoenfeld residuals test
- **p > 0.05**: PH assumption satisfied ✓
- **p < 0.05**: PH assumption violated ✗

---

## Best Practices

1. **Check censoring pattern**
   - High censoring (>50%) → limited statistical power
   - Informative censoring → biased results

2. **Don't ignore clinical knowledge**
   - Use known prognostic factors
   - Check variable distributions

3. **Report confidence intervals**
   - Not just point estimates
   - Shows uncertainty

4. **Validate on holdout data**
   - Train/test split
   - Cross-validation for small samples

5. **Check model assumptions**
   - PH assumption for Cox
   - Residual diagnostics

6. **Handle categorical variables properly**
   - One-hot encoding for Cox/RSF
   - Choose meaningful reference category

---

## Resources

**Documentation:**
- [lifelines](https://lifelines.readthedocs.io/)
- [scikit-survival](https://scikit-survival.readthedocs.io/)

**Tutorials:**
- [lifelines quickstart](https://lifelines.readthedocs.io/en/latest/Quickstart.html)
- [scikit-survival user guide](https://scikit-survival.readthedocs.io/en/stable/user_guide/index.html)
