# 淺度機器學習課程專案

本儲存庫記錄「Shallow Machine Learning」課程的課堂實作、作業提交、個人練習與筆記。內容以 Jupyter Notebook 為主，涵蓋 PCA/SVD、分類模型、影像與人臉分析等主題。

## 專案內容

- `InClassCoding/`: 課堂示範與練習（如 `PCA_tutorial.ipynb`、`Classification_tutorial.ipynb`、`facenetPytorch_demo.ipynb`）。
- `Homework/`: 作業與輸出檔（`SML_Work1_411278018.*`、`SML_Work2_411278018.*`、`SML_Work3_411278018.ipynb`）。
- `MyPractice/`: 個人延伸練習與資料/圖片。
- `Notes/`: 課堂筆記（目前為 `0304_PCA_Notes.ipynb`）。
- 根目錄工具腳本：`inspect_nb.py`、`patch_nb.py`、`refactor_notebook.py`、`matplotlib_config.py`。

## 建議環境

- Python `3.12+`
- 建議使用虛擬環境（專案內已有 `.venv/`）

## 安裝方式

### 方式 1：使用 `uv`（建議）

```bash
uv sync
```

### 方式 2：使用 `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 常用套件

目前 `requirements.txt` 以 PyTorch 生態為主：

- `torch`、`torchvision`、`torchaudio`
- `numpy`
- `pillow`

## 使用方式

1. 啟用虛擬環境。
2. 開啟 Jupyter Lab/Notebook。
3. 依資料夾目的執行對應 notebook：
   - 想看課堂流程：從 `InClassCoding/` 開始。
   - 想看作業成果：進入 `Homework/`。
   - 想看筆記整理：查看 `Notes/`。

## 備註

- 本專案為個人課程學習紀錄，檔案命名與內容依課程進度持續更新。
- 若僅需檢視結果，可直接閱讀 `Homework/` 中的 `html` 或 `pdf` 匯出檔。
