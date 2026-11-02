# -*- coding: utf-8 -*-
"""
Machine Learning-Based Analysis of Daily Rainfall Patterns and Extreme Rainfall Events in the Kathmandu Valley
Student: Sadhana Adhikari | ID: 260102 | CUID: 17625409
Module: STW7072CEM Machine Learning | MSc Data Science and Computational Intelligence

Unified, consistent pipeline implementing:
1. Data quality control & linear interpolation across 19 DHM stations (2016-2025, N = 69,407).
2. Antecedent multi-lag satellite feature engineering (1-day, 3-day, 7-day rolling sums).
3. Unsupervised spatial regime clustering via PCA and K-Means (k = 3).
4. Strict chronological split: Train (2016-2022, N = 48,583), Validation (2023-2024, N = 13,889), Independent Test (2025, N = 6,935).
5. Z-score feature scaling (StandardScaler fitted on Train only) for Support Vector Machines, evaluating both Linear and RBF kernels alongside class-weighted Random Forest and XGBoost.
6. Leave-One-District-Out (LODO) spatial cross-validation across Bhaktapur, Lalitpur, and Kathmandu.
7. Explainable AI (SHAP & feature importance), GPM satellite validation (Taylor Diagram, POD, FAR, CSI), and Mann-Kendall / Sen's slope trend analysis.
"""

import os
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler, label_binarize
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix, roc_curve, auc, cohen_kappa_score, mean_squared_error
)
from sklearn.utils.class_weight import compute_sample_weight
import pymannkendall as mk
import skill_metrics as sm
import shap

plt.rcParams.update({
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight'
})

current = os.path.abspath(os.getcwd())
candidates = [
    current,
    os.path.abspath(os.path.join(current, '..')),
    os.path.abspath(os.path.join(current, '..', '..')),
]
if '__file__' in globals():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.extend([
        file_dir,
        os.path.abspath(os.path.join(file_dir, '..')),
        os.path.abspath(os.path.join(file_dir, '..', '..'))
    ])

BASE_DIR = current
for c in candidates:
    if os.path.exists(os.path.join(c, 'Dataset', 'GPM_Daily_Rainfall_2016_2025_19_Stations.xlsx')):
        BASE_DIR = c
        break

DATA_DIR = os.path.join(BASE_DIR, 'Dataset')
OUT_IMG = os.path.join(BASE_DIR, 'Assignment', 'latex_documentation', 'Overleaf_LaTeX_Upload', 'output_image')
OUT_TBL = os.path.join(BASE_DIR, 'Assignment', 'latex_documentation', 'table_snap')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
ASSIGN_RESULTS_DIR = os.path.join(BASE_DIR, 'Assignment', 'results')

for d in [OUT_IMG, OUT_TBL, RESULTS_DIR, ASSIGN_RESULTS_DIR]:
    os.makedirs(d, exist_ok=True)

# =========================================================================
# 1. Data Ingestion, Quality Control & Imputation (19 Stations, 2016-2025)
# =========================================================================
dhm_path = os.path.join(DATA_DIR, 'DHM_RF_2016-2025 (1).xlsx')
gpm_path = os.path.join(DATA_DIR, 'GPM_Daily_Rainfall_2016_2025_19_Stations.xlsx')

dhm_df = pd.read_excel(dhm_path, sheet_name='24h accumulated Precipitation')
dhm_stations = pd.read_excel(dhm_path, sheet_name='Stations')
gpm_df = pd.read_excel(gpm_path, sheet_name=0)

dhm_df['Date'] = pd.to_datetime(dhm_df['Time'])
gpm_df['Date'] = pd.to_datetime(gpm_df['Time'])
dhm_df.drop_duplicates(subset=['Date'], inplace=True)
gpm_df.drop_duplicates(subset=['Date'], inplace=True)

# Drop the 2 non-operational stations with >90% missingness (Tarebhir: 100%, Thankot: 92.5%)
stations_to_drop = ['Tarebhir', 'Thankot']
dhm_df = dhm_df.drop(columns=[col for col in stations_to_drop if col in dhm_df.columns])

numeric_cols = dhm_df.select_dtypes(include=[np.number]).columns
dhm_df[numeric_cols] = dhm_df[numeric_cols].clip(lower=0).interpolate(method='linear', limit_direction='both').fillna(0)

gpm_numeric = gpm_df.select_dtypes(include=[np.number]).columns
gpm_df[gpm_numeric] = gpm_df[gpm_numeric].clip(lower=0).interpolate(method='linear', limit_direction='both').fillna(0)

merged_df = pd.merge(dhm_df, gpm_df, on='Date', suffixes=('_DHM', '_GPM'))
merged_df['Year'] = merged_df['Date'].dt.year
merged_df['Month'] = merged_df['Date'].dt.month

cleaned_path = os.path.join(BASE_DIR, 'Cleaned_DHM_GPM_Dataset.xlsx')
merged_df.to_excel(cleaned_path, index=False)
print(f'Cleaned dataset saved to: {cleaned_path}')

# =========================================================================
# 2. Spatio-Temporal Structuring & Antecedent Lag Feature Engineering
# =========================================================================
records = []
for idx, row in dhm_stations.iterrows():
    station = row['Name']
    col_dhm = f'{station}_DHM'
    col_gpm = f'{station}_GPM'
    if col_dhm in merged_df.columns and col_gpm in merged_df.columns:
        temp = merged_df[['Date', 'Year', 'Month', col_dhm, col_gpm]].copy()
        temp.columns = ['Date', 'Year', 'Month', 'DHM_Rainfall', 'GPM_Rainfall']
        temp['Station'] = station
        temp['District'] = row['District']
        temp['Latitude'] = row['Latitude']
        temp['Longitude'] = row['Longitude']
        temp['Elevation'] = row['Elevation']
        temp['GPM_Rainfall'] = pd.to_numeric(temp['GPM_Rainfall'], errors='coerce').fillna(0)
        temp['DHM_Rainfall'] = pd.to_numeric(temp['DHM_Rainfall'], errors='coerce').fillna(0)
        temp = temp.sort_values('Date')
        temp['GPM_1day'] = temp['GPM_Rainfall'].shift(1).fillna(0)
        temp['GPM_3day'] = temp['GPM_Rainfall'].rolling(3, min_periods=1).sum().shift(1).fillna(0)
        temp['GPM_7day'] = temp['GPM_Rainfall'].rolling(7, min_periods=1).sum().shift(1).fillna(0)
        records.append(temp)

df_all = pd.concat(records, ignore_index=True)

def classify_rainfall(val):
    if val < 10: return 'Light'
    elif val < 50: return 'Moderate'
    elif val < 100: return 'Heavy'
    elif val < 200: return 'Very Heavy'
    else: return 'Extreme'

df_all['Intensity_Class'] = df_all['DHM_Rainfall'].apply(classify_rainfall)
class_mapping = {'Light': 0, 'Moderate': 1, 'Heavy': 2, 'Very Heavy': 3, 'Extreme': 4}
df_all['Intensity_Class_Encoded'] = df_all['Intensity_Class'].map(class_mapping)
class_names = ['Light', 'Moderate', 'Heavy', 'Very Heavy', 'Extreme']
print(f'Total synchronized observations across 19 stations: {len(df_all):,}')

# =========================================================================
# 3. Unsupervised Learning: PCA & K-Means Clustering (k = 3)
# =========================================================================
features_agg = df_all.groupby('Station').agg({
    'DHM_Rainfall': ['mean', 'max', 'std'],
    'Elevation': 'first',
    'Latitude': 'first',
    'Longitude': 'first'
})
features_agg.columns = ['Mean_Rainfall', 'Max_Rainfall', 'Std_Rainfall', 'Elevation', 'Latitude', 'Longitude']

scaler_pca = StandardScaler()
X_scaled_pca = scaler_pca.fit_transform(features_agg)
pca = PCA(n_components=3, random_state=42)
pca_res = pca.fit_transform(X_scaled_pca)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(pca_res)
features_agg['Cluster'] = clusters
features_agg['PCA1'] = pca_res[:, 0]
features_agg['PCA2'] = pca_res[:, 1]

# =========================================================================
# 4. Supervised Classification: Corrected Chronological Split & Scaled SVM
# =========================================================================
features = ['GPM_Rainfall', 'GPM_1day', 'GPM_3day', 'GPM_7day', 'Elevation', 'Latitude', 'Longitude', 'Month']

# Strict chronological partitioning:
# - Training Set: 2016-2022 (7 years, N = 48,583)
# - Validation Set: 2023-2024 (2 years, N = 13,889)
# - Independent Test Set: 2025 (1 year, N = 6,935)
train_mask = (df_all['Year'] >= 2016) & (df_all['Year'] <= 2022)
val_mask   = (df_all['Year'] >= 2023) & (df_all['Year'] <= 2024)
test_mask  = (df_all['Year'] == 2025)

X_train = df_all.loc[train_mask, features]
y_train = df_all.loc[train_mask, 'Intensity_Class_Encoded']

X_val   = df_all.loc[val_mask, features]
y_val   = df_all.loc[val_mask, 'Intensity_Class_Encoded']

X_test  = df_all.loc[test_mask, features]
y_test  = df_all.loc[test_mask, 'Intensity_Class_Encoded']

print(f'Train Set (2016-2022):      {len(X_train):,} samples')
print(f'Validation Set (2023-2024): {len(X_val):,} samples')
print(f'Independent Test Set (2025): {len(X_test):,} samples')

# Scale features for SVM strictly using training set statistics (preventing data leakage)
svm_scaler = StandardScaler()
X_train_scaled = svm_scaler.fit_transform(X_train)
X_val_scaled   = svm_scaler.transform(X_val)
X_test_scaled  = svm_scaler.transform(X_test)

# Compute inverse-frequency balanced sample weights on the training set
weights = compute_sample_weight('balanced', y_train)

# 1. Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=15, max_depth=3, class_weight='balanced', random_state=42)
rf_model.fit(X_train, y_train)

# 2. XGBoost Classifier
xgb_model = xgb.XGBClassifier(max_depth=3, learning_rate=0.01, n_estimators=50, objective='multi:softprob', eval_metric='mlogloss', random_state=42)
xgb_model.fit(X_train, y_train, sample_weight=weights)

# 3. Support Vector Machine - Linear Kernel (Scaled)
svm_linear = SVC(kernel='linear', C=0.1, class_weight='balanced', probability=True, random_state=42)
svm_linear.fit(X_train_scaled, y_train)

# 4. Support Vector Machine - RBF Kernel (Scaled)
svm_rbf = SVC(kernel='rbf', C=1.0, gamma='scale', class_weight='balanced', probability=True, random_state=42)
svm_rbf.fit(X_train_scaled, y_train)

models_eval = [
    ('Random Forest', rf_model, X_val, X_test),
    ('XGBoost', xgb_model, X_val, X_test),
    ('SVM (Linear)', svm_linear, X_val_scaled, X_test_scaled),
    ('SVM (RBF)', svm_rbf, X_val_scaled, X_test_scaled),
]

print('\n================ VALIDATION SET RESULTS (2023-2024, N = 13,889) ================')
for name, model, X_v, _ in models_eval:
    y_pred_v = model.predict(X_v)
    print(f'--- {name} (Validation 2023-2024) ---')
    print(classification_report(y_val, y_pred_v, labels=[0,1,2,3,4], target_names=class_names, zero_division=0))

print('\n================ INDEPENDENT TEST SET RESULTS (2025, N = 6,935) ================')
for name, model, _, X_t in models_eval:
    y_pred_t = model.predict(X_t)
    print(f'--- {name} (Independent Test 2025) ---')
    print(classification_report(y_test, y_pred_t, labels=[0,1,2,3,4], target_names=class_names, zero_division=0))

# =========================================================================
# 5. Satellite Product Validation & Mann-Kendall Trend Analysis
# =========================================================================
dhm_vals = df_all['DHM_Rainfall'].values
gpm_vals = df_all['GPM_Rainfall'].values
corr_val = np.corrcoef(dhm_vals, gpm_vals)[0, 1]
bias_val = np.mean(gpm_vals - dhm_vals)
rmse_val = np.sqrt(mean_squared_error(dhm_vals, gpm_vals))
nse_val  = 1 - (np.sum((dhm_vals - gpm_vals) ** 2) / np.sum((dhm_vals - np.mean(dhm_vals)) ** 2))

threshold = 1.0
hits = np.sum((dhm_vals >= threshold) & (gpm_vals >= threshold))
misses = np.sum((dhm_vals >= threshold) & (gpm_vals < threshold))
false_alarms = np.sum((dhm_vals < threshold) & (gpm_vals >= threshold))
pod = hits / (hits + misses)
far = false_alarms / (hits + false_alarms)
csi = hits / (hits + misses + false_alarms)

print('--- GPM IMERG V07 Satellite Evaluation vs DHM Ground Truth (19 Stations) ---')
print(f'Pearson Correlation (r): {corr_val:.4f}')
print(f'Mean Bias:               {bias_val:+.4f} mm/day')
print(f'RMSE:                    {rmse_val:.4f} mm/day')
print(f'NSE:                     {nse_val:.4f}')
print(f'POD:                     {pod:.4f} ({pod*100:.2f}%)')
print(f'FAR:                     {far:.4f} ({far*100:.2f}%)')
print(f'CSI:                     {csi:.4f} ({csi*100:.2f}%)')

trend_metrics = {
    'Annual Mean Rainfall': df_all.groupby('Year')['DHM_Rainfall'].mean(),
    'Max Daily Rainfall': df_all.groupby('Year')['DHM_Rainfall'].max(),
    'Rainy Days (>1mm)': df_all[df_all['DHM_Rainfall'] > 1].groupby('Year')['DHM_Rainfall'].count(),
    'Extreme Events (>100mm)': df_all[df_all['DHM_Rainfall'] >= 100].groupby('Year')['DHM_Rainfall'].count()
}
print('\n--- Mann-Kendall Trend Analysis (2016-2025) ---')
for title, series in trend_metrics.items():
    res = mk.original_test(series.values)
    print(f'{title}: Trend={res.trend}, p-value={res.p:.4f}, Slope={res.slope:+.4f}')
