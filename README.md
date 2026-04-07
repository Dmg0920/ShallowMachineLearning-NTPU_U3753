# 淺度機器學習 (Shallow Machine Learning) 課程專案

這是一個關於「淺度機器學習」課程的學習記錄與作業存放庫。本專案包含了課堂練習、作業實作、個人練習以及相關的筆記與資料。

## 🚀 專案概述

本專案主要探討經典的機器學習技術，重點包括：
- **降維技術 (Dimensionality Reduction)**：PCA (主成分分析)、SVD (奇異值分解)。
- **特徵提取 (Feature Extraction)**：Eigenfaces (特徵臉) 應用於人臉分析。
- **數據視覺化**：Digits (手寫數字) 與影像處理。
- **統計分析**：協方差矩陣、線性相關性與數據預處理。

## 📂 目錄結構

```text
.
├── Homework/               # 課程作業 (如 SML_Work1, SML_Work2)
│   ├── run_face_analysis.py # 人臉分析腳本
│   └── *.ipynb, *.pdf      # 作業實作與匯出文件
├── InClassCoding/          # 課堂實作範例
│   ├── PCA_SVD_Digits.ipynb
│   ├── PCA_tutorial.ipynb
│   └── data/               # 課堂使用的數據集
├── MyPractice/             # 個人練習與實驗
├── Notes/                  # 課程筆記 (Jupyter Notebook 格式)
├── data/                   # 共用數據集
├── requirements.txt        # 專案依賴清單
└── pyproject.toml          # 專案配置 (使用 uv 管理)
```

## 🛠️ 環境設定

本專案建議使用 Python 3.12+ 以及 [uv](https://github.com/astral-sh/uv) 進行管理。

### 1. 安裝依賴

你可以使用 `uv` 快速同步環境：

```bash
uv sync
```

或者使用傳統的 `pip`：

```bash
pip install -r requirements.txt
```

### 2. 主要依賴庫

- `numpy`, `scipy`: 數值計算與線性代數。
- `pandas`: 數據處理與分析。
- `scikit-learn`: 機器學習算法實作。
- `matplotlib`, `seaborn`: 數據視覺化。
- `scikit-image`, `Pillow`: 影像處理。

## 📝 重點筆記內容

- **0304 PCA Notes**: 深入探討 PCA 的數學原理、協方差矩陣以及如何解決高維度數據的計算與線性相關問題。
- **Face Analysis**: 實作 Eigenfaces 技術，進行人臉重建與降維分析。

## 🤝 貢獻與使用

這是我個人的學習記錄，歡迎參考。如果你發現任何錯誤或有改進建議，請隨時提出。

---
*Last updated: 2026-04-07*
