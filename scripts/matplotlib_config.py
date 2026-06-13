import matplotlib.pyplot as plt
import matplotlib as mpl
import os

def init_mpl_taiwan():
    """
    一勞永逸的繪圖設定：優化中文字型與視覺外觀
    """
    # 1. 字型優先順序 (PingFang 是 macOS 最現代好看的字型)
    # 如果您想要更專業的論文感，可以把 'Songti TC' 放在最前面
    fonts = ['PingFang TC', 'Heiti TC', 'Lantinghei TC', 'Songti TC', 'Arial Unicode MS']
    
    plt.rcParams['font.sans-serif'] = fonts + plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 修正負號顯示
    
    # 2. 視覺優化：讓圖表更有「質感」
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['axes.labelcolor'] = '#333333'
    plt.rcParams['xtick.color'] = '#333333'
    plt.rcParams['ytick.color'] = '#333333'
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['font.size'] = 11
    plt.rcParams['figure.dpi'] = 120  # 高清顯示

    print(f"✅ 已載入好看的中文字型設定：{fonts[0]}")

# 執行初始化
if __name__ == "__main__":
    init_mpl_taiwan()
