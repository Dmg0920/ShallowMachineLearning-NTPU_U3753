# Shallow Machine Learning 課程專案

本儲存庫整理「Shallow Machine Learning」課程的課堂實作、作業、個人練習與筆記。主要工作型態是 Jupyter Notebook，主題包含 PCA/SVD、分類模型、人臉資料處理、PyTorch CNN，以及影像去模糊實驗。

## 專案結構

| 路徑 | 用途 |
| --- | --- |
| `Homework/` | 作業 notebook、規格文件、輸出圖表與交件用 HTML/PDF。 |
| `Homework/spec/` | 作業規格與實作約束，例如 Work4 spec。 |
| `Homework/DeblurCNN_2026/` | Work4 影像去模糊資料、模型與輸出。 |
| `InClassCoding/` | 課堂範例與老師提供的程式碼；此目錄是 Git submodule。 |
| `MyPractice/` | 個人延伸練習、實驗資料與影像素材。 |
| `Notes/` | 課堂筆記 notebook。 |
| `inspect_nb.py` | 檢查 notebook cell 內容的輔助腳本。 |
| `patch_nb.py` | 針對 notebook JSON 進行小範圍修補的輔助腳本。 |
| `refactor_notebook.py` | notebook 結構整理與批次修改工具。 |
| `matplotlib_config.py` | macOS 中文字型與圖表樣式設定。 |

## 環境需求

- Python 3.12+
- 建議使用專案內 `.venv`
- Apple Silicon / macOS 可用於開發、分析與 CPU/MPS 推論
- CUDA 訓練請在 Windows/WSL2 或對應 CUDA 環境另外安裝相容 PyTorch wheel

目前有兩份依賴來源，角色不同：

- `requirements.txt`: notebook runtime 主要依賴，包含 `numpy`、`pandas`、`scikit-learn`、`scipy`、`matplotlib`、`seaborn`、`scikit-image`、`openpyxl`、`torch`、`torchvision`、`torchaudio`、`facenet-pytorch`、`ipykernel` 等。
- `pyproject.toml`: uv 專案設定、dev tools、Ruff 與 BasedPyright 設定；目前不是完整 runtime manifest。

不要只跑 `uv sync` 就假設所有 notebook 依賴都已安裝。

## 安裝

建議使用 `uv` 建立環境，並用 `requirements.txt` 安裝 notebook runtime：

```bash
uv venv --python 3.12
source .venv/bin/activate
uv sync --group dev
uv pip install -r requirements.txt
python -m ipykernel install --user --name ml-course --display-name "Python (ml_course)"
```

如果不用 `uv`：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install ipykernel ruff basedpyright pandas-stubs
python -m ipykernel install --user --name ml-course --display-name "Python (ml_course)"
```

如果要用瀏覽器開 Jupyter Lab，另外安裝：

```bash
python -m pip install jupyterlab nbconvert
python -m jupyter lab
```

## 常用工作流程

### 開啟 notebook

1. 啟用 `.venv`。
2. 在 VS Code、Cursor、Jupyter Lab 或 Jupyter Notebook 中選擇 `Python (ml_course)` kernel。
3. 依目的進入對應資料夾：
   - 課堂內容：`InClassCoding/`
   - 作業成果：`Homework/`
   - 個人練習：`MyPractice/`
   - 課堂筆記：`Notes/`

### 執行作業 notebook

作業交件前應使用 Restart & Run All 重新執行，確認文字、表格、圖與輸出檔一致。若要用 CLI 執行並覆寫 notebook：

```bash
python -m jupyter nbconvert \
  --to notebook \
  --execute \
  --inplace Homework/SML_Work4_411278018.ipynb \
  --ExecutePreprocessor.timeout=7200 \
  --ExecutePreprocessor.kernel_name=python3
```

匯出 HTML：

```bash
python -m jupyter nbconvert \
  --to html Homework/SML_Work4_411278018.ipynb \
  --output SML_Work4_411278018.html \
  --output-dir Homework
```

### 檢查 Python helper

```bash
ruff check inspect_nb.py patch_nb.py refactor_notebook.py matplotlib_config.py Homework/run_face_analysis.py
basedpyright inspect_nb.py patch_nb.py refactor_notebook.py matplotlib_config.py Homework/run_face_analysis.py
```

## 作業維護規則

- `Homework/SML_Work*_411278018.ipynb` 是主要交件來源。
- `Homework/spec/` 與 `Homework/HW3_spec.md` 這類規格文件優先於口頭猜測；修改 notebook 前先讀 spec。
- 結果敘述中的 accuracy、fit time、PSNR、SSIM 等數字應盡量由程式輸出動態產生，避免 markdown hardcode 後與 cell output 不一致。
- notebook 內路徑使用 `pathlib.Path` 與相對路徑，不寫死本機絕對路徑。
- 大型訓練輸出、臨時檔與非交件輸出提交前要先確認是否必要。
- 若修改 `InClassCoding/`，那是 submodule 內部變更；需要在 submodule 本身處理 commit，再回到本 repo 更新 submodule pointer。

## Git 注意事項

`.gitignore` 已排除常見暫存與大型資料型態：

- Python cache: `__pycache__/`、`*.pyc`
- 虛擬環境: `.venv/`
- Jupyter checkpoint: `.ipynb_checkpoints/`
- macOS 暫存: `.DS_Store`
- 常見輸出目錄: `output/`、`outputs/`、`results/`、`figures/`
- 大型資料: `*.mat`、`*.pkl`、`data/raw/`
- 私密檔案: `.env*`、`secrets.json`、`credentials.json`

作業 HTML/PDF、CSV、模型權重或圖片是否納入版本控制，依當次交件需求決定；不要直接 `git add .` 混入 IDE 設定、快取、未確認輸出或 submodule dirty state。

## 常見問題

### `uv sync` 後 notebook import 失敗

原因通常是 `pyproject.toml` 尚未收錄完整 runtime 依賴。執行：

```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Jupyter 找不到 kernel

重新註冊 kernel：

```bash
source .venv/bin/activate
python -m ipykernel install --user --name ml-course --display-name "Python (ml_course)"
```

### CUDA / PyTorch 安裝不符合訓練機

`requirements.txt` 目前鎖定一般 PyTorch 套件版本。若要在 RTX 4060 + CUDA 上訓練，請依該環境的 CUDA 版本安裝對應 PyTorch wheel，不要直接沿用 macOS 環境假設。
