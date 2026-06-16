# RADCURE Dataset Instructions

This assignment uses the **RADCURE** clinical dataset from The Cancer Imaging Archive.

## Download Instructions

### Option 1: Download from TCIA (Recommended)

1. Visit: [https://www.cancerimagingarchive.net/collection/radcure/](https://www.cancerimagingarchive.net/collection/radcure/)
2. Scroll to **"Data Access"** section
3. Find the **"Clinical data"** row in the table
4. Click the **"DOWNLOAD"** button (463KB XLSX file)
5. Save as `RADCURE-clinical-data.xlsx` in this `data/` directory

### Option 2: Download from Blackboard

1. Go to the Assignment 4 folder on Blackboard
2. Download the provided `RADCURE-clinical-data.xlsx` file
3. Save it in this `data/` directory

## Loading the Data

### In Python

```python
import pandas as pd

# Load RADCURE clinical data
data = pd.read_excel('data/RADCURE-clinical-data.xlsx', sheet_name='RADCURE_TCIA_Clinical_r2_offset')

# Or if you converted to CSV:
data = pd.read_csv('data/RADCURE-clinical-data.csv')

print(f"Dataset shape: {data.shape}")
print(f"Columns: {list(data.columns)}")
```

## Key Columns for Survival Analysis

### Time-to-Event Variables

- **`Length FU`** - Follow-up duration in years
- **`Status`** - Vital status (Dead, Alive)

### Clinical Covariates (Examples)

**Demographics:**
- `Age` - Patient age at diagnosis
- `Sex` - Male/Female

**Disease Characteristics:**
- `Disease_Site` - Cancer subsite (Oropharynx, Larynx, etc.)
- `T_Stage` - Tumor stage (T1, T2, T3, T4)
- `N_Stage` - Nodal stage (N0, N1, N2, N3)
- `Stage` - TNM overall stage (I, II, III, IV)
- `HPV` - HPV status (positive/negative/unknown)

**Treatment:**
- `Chemo` - Received chemotherapy (Yes/none)
- `Dose` - Radiation dose in Gray

**Other:**
- `Smoking_Status` - Non-Smoker/Ex-Smoker/Current
- `Tx Modality` - RT alone, ChemoRT
- `ECOG PS` - Performance status

## Data Preparation Tips

### 1. Handle Missing Values

```python
# Check missing data
data.isnull().sum()

# Drop rows with missing survival time or event
data = data.dropna(subset=['Survival_time_in_days', 'Death'])
```

### 2. Create Binary Grouping Variables

```python
# Age groups
data['Age_Group'] = pd.cut(data['Age'], bins=[0, 60, 100], labels=['≤60', '>60'])

# Stage groups (suggest grouping by numerical stage, i.e., [1,2,3,4] versus [1A, 1B, ...])
data['Stage_Group'] = data['Overall_Stage'].map({
    'I': 'Early', 'II': 'Early',
    'III': 'Advanced', 'IV': 'Advanced'
})
```

### 3. Encode Categorical Variables for Cox/RSF

```python
# One-hot encoding for categorical covariates
data_encoded = pd.get_dummies(data, columns=['Disease_Site', 'T_Stage'], drop_first=True)

# Event indicator --> binary
data.Status = data.Status == "Dead"

```

## Data Citation

**Required citation for any use of RADCURE data:**

Welch, M. L., Kim, S., Hope, A., Huang, S. H., Lu, Z., Marsilla, J., Kazmierski, M., Rey-McIntyre, K., Patel, T., O'Sullivan, B., Waldron, J., Kwan, J., Su, J., Soltan Ghoraie, L., Chan, H. B., Yip, K., Giuliani, M., Princess Margaret Head And Neck Site Group, Bratman, S., … Tadic, T. (2023). Computed Tomography Images from Large Head and Neck Cohort (RADCURE) (Version 4) [Dataset]. The Cancer Imaging Archive. https://doi.org/10.7937/J47W-NM11

## License

RADCURE clinical data is licensed under **CC BY 4.0** (Creative Commons Attribution 4.0 International).

## Troubleshooting

**File not found error?**
- Make sure the file is in the `data/` directory
- Check the filename matches exactly

**Excel file issues?**
- Convert to CSV: Open in Excel/Numbers, Save As → CSV
- Use `data.to_csv('data/RADCURE-clinical-data.csv', index=False)`

**Column name errors?**
- Print all column names: `print(data.columns.tolist())`
- Column names may have been updated in newer versions
