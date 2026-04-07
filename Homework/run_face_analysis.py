
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces

# 載入 Olivetti Faces 資料集
faces_data = fetch_olivetti_faces(shuffle=False)
X = faces_data.data * 255
mean_face_vec = np.mean(X, axis=0)
X_centered = X - mean_face_vec

# 完整 SVD 分解
U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)

# 1. 奇異值能量分析
energy = s**2
total_energy = np.sum(energy)
cum_energy = np.cumsum(energy) / total_energy

# 找出能量門檻對應的 q
q_90 = int(np.searchsorted(cum_energy, 0.90) + 1)
q_95 = int(np.searchsorted(cum_energy, 0.95) + 1)
q_99 = int(np.searchsorted(cum_energy, 0.99) + 1)

print(f"90% 能量所需成分數 q: {q_90}")
print(f"95% 能量所需成分數 q: {q_95}")
print(f"99% 能量所需成分數 q: {q_99}")

# 2. 視覺化前 10 個 Eigenfaces（右奇異向量）
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.flat):
    # Eigenface 是 Vt 的行向量
    eigenface = Vt[i].reshape(64, 64)
    # 使用發散色階（RdBu_r）顯示特徵臉的正負變化
    im = ax.imshow(eigenface, cmap='RdBu_r') 
    ax.set_title(f'Eigenface {i+1}')
    ax.axis('off')
plt.suptitle('前 10 個特徵臉 (Eigenfaces)', fontsize=14, fontweight='bold')
plt.savefig('Homework/face_analysis_eigenfaces.png')
plt.close()

# 3. 不同 q 值下的人臉重建測試
def psnr_metric(orig, recon):
    mse = np.mean((orig - recon)**2)
    if mse < 1e-10: return float('inf')
    return 20 * np.log10(255.0 / np.sqrt(mse))

test_indices = [0, 100, 200] # 選三個不同人的臉測試
qs = [10, 30, 50, 100, 200]

fig, axes = plt.subplots(len(test_indices), len(qs)+1, figsize=(15, 8))
for i, idx in enumerate(test_indices):
    orig = X[idx]
    # 原始圖
    axes[i, 0].imshow(orig.reshape(64, 64), cmap='gray')
    if i == 0: axes[i, 0].set_title('Original')
    axes[i, 0].axis('off')
    
    for j, q in enumerate(qs):
        # 重建公式: (U[idx, :q] * s[:q]) @ Vt[:q, :] + mean_face
        recon = (U[idx, :q] * s[:q]) @ Vt[:q, :] + mean_face_vec
        recon = np.clip(recon, 0, 255)
        p_val = psnr_metric(orig, recon)
        
        axes[i, j+1].imshow(recon.reshape(64, 64), cmap='gray')
        if i == 0: axes[i, j+1].set_title(f'q={q}')
        axes[i, j+1].set_xlabel(f'{p_val:.1f} dB')
        axes[i, j+1].axis('off')

plt.suptitle('不同 q 值下的人臉重建品質比較', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('Homework/face_reconstruction_results.png')
plt.close()
