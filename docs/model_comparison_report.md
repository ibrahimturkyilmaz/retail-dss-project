# 📊 Faz 3: Model Karşılaştırması — Prophet vs XGBoost

**Proje:** RetailDSS — Akıllı Perakende Karar Destek Sistemi  
**Tarih:** 2026-02-15  

---

## 1. Amaç

İki farklı makine öğrenmesi modelinin (Facebook Prophet ve XGBoost) perakende satış tahmini performansını karşılaştırarak, hangi modelin hangi koşullarda daha başarılı olduğunu belirlemek.

---

## 2. Geliştirme Planı

### Adım 1: Veri Hazırlığı
- Mevcut `sales_s1_p1.csv` verisini kullan (2 yıl, 730 gün)
- Feature engineering:
  - **Zaman özellikleri:** `day_of_week`, `month`, `is_weekend`, `quarter`
  - **Lag özellikleri:** `lag_1`, `lag_7`, `lag_30` (geçmiş satışlar)
  - **Rolling özellikleri:** `rolling_mean_7`, `rolling_std_7`
  - **Dış değişkenler:** `temperature`, `rain` (Open-Meteo API)

### Adım 2: XGBoost Model Eğitimi (Google Colab)
```python
import xgboost as xgb
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Feature matrix oluştur
features = ['day_of_week', 'month', 'is_weekend', 'quarter',
            'lag_1', 'lag_7', 'lag_30',
            'rolling_mean_7', 'rolling_std_7',
            'temperature', 'rain']

X = df[features]
y = df['y']

# Zaman serisi cross-validation (5 fold)
tscv = TimeSeriesSplit(n_splits=5)

model = xgb.XGBRegressor(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    early_stopping_rounds=50,
    random_state=42
)

# Eğitim + değerlendirme
for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    model.fit(X_train, y_train, 
              eval_set=[(X_test, y_test)], 
              verbose=False)
```

### Adım 3: Prophet Model Eğitimi (Mevcut)
- `interval_width=0.5`, `changepoint_prior_scale=0.01`
- Hava durumu regressörleri (sıcaklık + yağış)
- Türkiye tatilleri

### Adım 4: Performans Karşılaştırması

| Metrik | Açıklama | Formül |
|--------|----------|--------|
| **MAE** | Ortalama Mutlak Hata | `mean(|y - ŷ|)` |
| **RMSE** | Kök Ortalama Kare Hata | `sqrt(mean((y - ŷ)²))` |
| **MAPE** | Yüzde Cinsinden Hata | `mean(|y - ŷ| / y) × 100` |
| **R²** | Açıklanan Varyans Oranı | `1 - SS_res / SS_tot` |

```python
# Karşılaştırma sonuçlarını CSV'ye kaydet
comparison = pd.DataFrame({
    'Model': ['Prophet', 'XGBoost'],
    'MAE': [prophet_mae, xgb_mae],
    'RMSE': [prophet_rmse, xgb_rmse],
    'MAPE': [prophet_mape, xgb_mape],
    'R2': [prophet_r2, xgb_r2],
    'Training_Time_Sec': [prophet_time, xgb_time]
})
comparison.to_csv('model_comparison.csv', index=False)
```

### Adım 5: Feature Importance (XGBoost Avantajı)
```python
import matplotlib.pyplot as plt

# XGBoost feature importance grafiği
fig, ax = plt.subplots(figsize=(10, 6))
xgb.plot_importance(model, ax=ax, importance_type='gain', max_num_features=10)
plt.title('XGBoost — Özellik Önem Sıralaması')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150)
```

### Adım 6: Frontend Entegrasyonu
- Model & AI sekmesine karşılaştırma tablosu ekle
- Her iki modelin MAPE grafiği (bar chart)
- Feature importance görselleştirme

---

## 3. Beklenen Sonuçlar

| Özellik | Prophet | XGBoost |
|---------|---------|---------|
| **Güçlü Yönü** | Trend + Mevsimsellik ayrıştırması, tatil etkisi | Karmaşık non-linear ilişkiler, feature engineering |
| **Zayıf Yönü** | Çok değişkenli ilişkilerde sınırlı | Mevsimselliği kendisi öğrenemez (manual feature gerek) |
| **Eğitim Süresi** | ~30 sn | ~5 sn |
| **Yorumlanabilirlik** | Yüksek (decomposition) | Orta (SHAP/feature importance) |
| **En İyi Senaryo** | Güçlü mevsimsellik + tatil etkisi | Çok sayıda dış değişken + non-linear patternlar |

### Beklenen MAPE Aralığı
- **Prophet:** %15-25 (mevsimsellik güçlü olduğunda daha iyi)
- **XGBoost:** %10-20 (yeterli feature engineering ile daha iyi)

---

## 4. Akademik Kaynaklar

| # | Kaynak | İlgisi |
|---|--------|--------|
| [1] | **Chen, T., & Guestrin, C. (2016).** "XGBoost: A Scalable Tree Boosting System." *KDD '16*, 785-794. | XGBoost'un orijinal makalesi. |
| [2] | **Taylor, S. J., & Letham, B. (2018).** "Forecasting at Scale." *The American Statistician*, 72(1). | Prophet'in orijinal makalesi. |
| [3] | **Makridakis, S., et al. (2018).** "Statistical and ML Forecasting Methods." *PLOS ONE*. | İki yaklaşımın karşılaştırması. |
| [4] | **Fildes, R., et al. (2022).** "Forecasting Competitions: Their Role in Advancing Forecasting." *IJF*. | Model karşılaştırma metodolojisi. |
| [5] | **Ceylan, S. (2024).** "Perakende Satış Tahmini." *YTÜ, YL Tezi.* | Türkçe perakende ML karşılaştırması. |
| [6] | **Lundberg, S. M., & Lee, S. I. (2017).** "A Unified Approach to Interpreting Model Predictions." *NeurIPS.* | SHAP — XGBoost yorumlanabilirlik. |

---

## 5. Dosya Yapısı

```
retail-dss-project/
├── docs/
│   ├── prophet_optimization_report.md    ← Mevcut
│   └── model_comparison_report.md        ← Yeni (bu dosya)
├── backend/
│   ├── import_forecasts.py               ← Mevcut
│   └── main.py                           ← /comparison endpoint
└── frontend/
    └── src/pages/Settings.jsx            ← Karşılaştırma UI
```
