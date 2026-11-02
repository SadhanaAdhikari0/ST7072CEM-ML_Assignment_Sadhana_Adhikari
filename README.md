# Machine Learning-Based Analysis of Daily Rainfall Patterns and Extreme Rainfall Events in the Kathmandu Valley

**Student:** Sadhana Adhikari  
**Student ID:** 260102 | **CUID:** 17625409  
**Module:** STW7072CEM Machine Learning  
**Programme:** MSc Data Science and Computational Intelligence  
**Institution:** Softwarica College of IT and E-Commerce, Coventry University

---

## Project Overview

This project implements a comprehensive machine learning framework for rainfall intensity classification using:
- **19 DHM (Department of Hydrology and Meteorology) ground stations** (2016-2025)
- **GPM IMERG V07 satellite precipitation data** (2016-2025)

### Three Core Objectives:
1. **Spatial & Temporal Variability Analysis** – PCA + K-Means Clustering
2. **Rainfall Intensity Classification** – Random Forest, XGBoost, SVM
3. **Long-Term Trend Analysis** – Mann-Kendall Test + Sen's Slope

---

## Directory Structure

```
SA_Assignment_ML/
├── Dataset/
│   ├── DHM_RF_2016-2025 (1).xlsx    # DHM ground observations (19 stations)
│   └── GPM_Daily_Rainfall_2016_2025_19_Stations.xlsx  # GPM satellite data (19 stations)
│
├── Assignment/
│   ├── full_code/
│   │   ├── ML_Rainfall_Analysis.py    # Main analysis script (620 lines)
│   │   ├── ML_Rainfall_Analysis.ipynb # Fully executed Jupyter Notebook with inline plots
│   │   ├── dashboard.py               # 3D Streamlit interactive web dashboard
│   │   └── requirements.txt           # Python dependency specifications
│   │
│   ├── latex_documentation/
│   │   ├── ML_Assignment_Paper.tex  # IEEE 2-column paper
│   │   ├── output_image/            # All generated figures
│   │   ├── table_snap/              # All generated tables
│   │   └── code_snap/               # Code snapshots
│   │
│   └── Base_Paper/
│       ├── 1.pdf
│       ├── 4.KirpaSOHAM_2024_DOI.pdf
│       └── Earth and Space Science - 2020 - Sharma...pdf
│
├── Perposal/
│   ├── MLAssignmentNewProposal.tex   # Research proposal
│   ├── Perposal.pdf
│   └── Rainfall Analysis Workflow Infographic.png
│
└── coursework_requirements/
    ├── STW7072CEM Machine Learning...pdf
    └── Experimental_Paper_Blueprint.pdf
```

---

## Prerequisites

### Python Version
- Python 3.10 or higher

### Required Libraries
Install all dependencies:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn plotly xgboost scipy pymannkendall openpyxl shap kaleido
```

### LaTeX (for paper compilation)
- MiKTeX or TeX Live with IEEEtran class

---

## Execution Instructions

### Step 1: Run the Analysis Script

```bash
cd Assignment/full_code/
python ML_Rainfall_Analysis.py
```

This script will:
1. Load and preprocess DHM and GPM datasets
2. Perform feature engineering (spatial, temporal, antecedent features)
3. Run PCA and K-Means clustering (Objective 1)
4. Train and evaluate RF, XGBoost, SVM classifiers (Objective 2)
5. Perform Mann-Kendall trend analysis (Objective 3)
6. Generate SHAP explainability analysis
7. Save all figures to `latex_documentation/output_image/`
8. Save all tables to `latex_documentation/table_snap/`
9. Launch interactive Streamlit dashboard (`dashboard.py`)

**Estimated runtime:** 2-5 minutes (depends on hardware)

### Step 2: Run the Animated Dashboard

```bash
cd Assignment/full_code/
streamlit run dashboard.py
```

This will automatically launch the **Animated Streamlit Dashboard** in your default web browser (usually at `http://localhost:8501`).

The dashboard includes:
- **Overview:** Key statistics, pie charts, and animated Year-over-Year bar charts.
- **Data Analysis:** Monthly/seasonal distributions, DHM vs GPM validation.
- **Clustering & PCA:** 3D and 2D Scatter plot visualisations of spatial regimes.
- **Live Prediction Engine:** Interactive UI with pulsing animations to predict rainfall categories in real-time.
- **Trend Analysis:** Annual trends and daily time series.

### Step 3: Compile the LaTeX Paper

```bash
cd Assignment/latex_documentation/
pdflatex ML_Assignment_Paper.tex
bibtex ML_Assignment_Paper
pdflatex ML_Assignment_Paper.tex
pdflatex ML_Assignment_Paper.tex
```

---

## Output Files

### Figures (output_image/)
| File | Description |
|------|-------------|
| `fig1_study_area_map.png` | Kathmandu Valley 3D Topographical Map |
| `elevation_bias.png` | Topographical bias validation |
| `missing_value_heatmap.png` | Missing value pattern across stations |
| `dhm_vs_gpm_scatter.png` | DHM vs GPM validation scatter plots |
| `class_distribution.png` | Rainfall intensity class distribution |
| `seasonal_distribution.png` | Seasonal rainfall distributions |
| `monthly_mean_rainfall.png` | Monthly mean daily rainfall |
| `correlation_matrix.png` | Feature correlation matrix |
| `normalization_comparison.png` | Before/after normalisation |
| `pca_analysis.png` | PCA scree plot and loadings |
| `pca_2d_scatter.png` | PCA 2D scatter plot |
| `kmeans_optimal_k.png` | Elbow and silhouette analysis |
| `kmeans_clusters_2d.png` | K-Means clusters in PCA space |
| `cluster_radar.png` | Cluster radar profiles |
| `station_heatmap.png` | Station feature heatmap |
| `confusion_matrices.png` | Confusion matrices (RF, XGB, SVM) |
| `roc_curves.png` | Multi-class ROC curves |
| `feature_importance.png` | Feature importance (RF, XGBoost) |
| `shap_importance.png` | SHAP feature importance |
| `cv_comparison.png` | Cross-validation comparison |
| `annual_trend.png` | Annual rainfall trend |
| `extreme_rainfall_frequency.png` | Extreme event frequency |
| `max_daily_rainfall_heatmap.png` | Maximum daily rainfall heatmap |
| `boxplot_stations.png` | Station rainfall box plots |
| `monthly_variability.png` | Monthly variability by station |

### Tables (table_snap/)
| File | Description |
|------|-------------|
| `table_descriptive_stats.png` | Descriptive statistics |
| `table_gpm_validation.png` | GPM validation metrics |
| `table_cluster_characteristics.png` | K-Means cluster summary |
| `table_model_comparison.png` | Model performance comparison |
| `table_complexity.png` | Time & space complexity |
| `table_perclass_metrics.png` | Per-class classification metrics |
| `table_trend_results.png` | Mann-Kendall trend results |
| `table_seasonal_trends.png` | Seasonal trend analysis |

---

## Machine Learning Methods Summary

| Method | Type | Purpose |
|--------|------|---------|
| PCA | Unsupervised | Dimensionality reduction |
| K-Means | Unsupervised | Station clustering |
| Random Forest | Supervised | Rainfall classification |
| XGBoost | Supervised | Rainfall classification |
| SVM (RBF) | Supervised | Rainfall classification |
| Mann-Kendall | Statistical | Trend detection |
| Sen's Slope | Statistical | Trend magnitude |
| SHAP | Explainability | Feature importance |

---

## Key References

1. Sharma et al. (2020) - Satellite precipitation evaluation
2. Khanal et al. (2024) - Precipitation extreme analysis
3. Chhetri et al. (2021) - CMIP6 precipitation projections
4. Breiman (2001) - Random Forest
5. Chen & Guestrin (2016) - XGBoost
6. Vapnik (1995) - Support Vector Machines

---

© 2026 Sadhana Adhikari | STW7072CEM Machine Learning Assignment
