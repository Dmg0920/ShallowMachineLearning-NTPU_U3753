import json

with open("Homework/SML_Work2_411278018.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

old_str = """print(f"{'影像類型':<25} | {'Patch':<6} | {'目標比例':<8} | {'實際比例':<8} | {'PSNR':<8}")
print("-" * 75)

for idx, (name, img) in enumerate(images_compare.items()):
    ax = axes[idx]
    for p in patch_sizes_comp:
        p_mat, meta = extract_patches(img, p)
        p_mean = p_mat.mean(axis=0, keepdims=True)
        p_centered = p_mat - p_mean
        Up, sp, Vtp = np.linalg.svd(p_centered, full_matrices=False)
        
        ratios_plot = []
        psnrs_plot = []
        
        for tr in target_ratios_comp:
            best_q = 0
            for q_try in range(1, len(sp) + 1):
                if patch_compression_ratio(256, 256, p, q_try) >= tr:
                    best_q = q_try
                else:
                    break
            
            if best_q > 0:
                p_rec = (Up[:, :best_q] * sp[:best_q]) @ Vtp[:best_q, :] + p_mean
                img_rec = np.clip(reconstruct_from_patches(p_rec, meta, p), 0, 255)
                actual_r = patch_compression_ratio(256, 256, p, best_q)
                p_val = psnr(img, img_rec)
                
                ratios_plot.append(actual_r)
                psnrs_plot.append(p_val)
                print(f"{name:<25} | {p:>2}x{p:<2} | {tr:>8} | {actual_r:>8.1f} | {p_val:>8.2f}")
        
        ax.plot(ratios_plot, psnrs_plot, 'o-', color=colors_map_comp[p], label=f'Patch {p}x{p}')"""

new_str = """data_summary = []

for idx, (name, img) in enumerate(images_compare.items()):
    ax = axes[idx]
    for p in patch_sizes_comp:
        p_mat, meta = extract_patches(img, p)
        p_mean = p_mat.mean(axis=0, keepdims=True)
        p_centered = p_mat - p_mean
        Up, sp, Vtp = np.linalg.svd(p_centered, full_matrices=False)
        
        ratios_plot = []
        psnrs_plot = []
        
        for tr in target_ratios_comp:
            best_q = 0
            for q_try in range(1, len(sp) + 1):
                if patch_compression_ratio(256, 256, p, q_try) >= tr:
                    best_q = q_try
                else:
                    break
            
            if best_q > 0:
                p_rec = (Up[:, :best_q] * sp[:best_q]) @ Vtp[:best_q, :] + p_mean
                img_rec = np.clip(reconstruct_from_patches(p_rec, meta, p), 0, 255)
                actual_r = patch_compression_ratio(256, 256, p, best_q)
                p_val = psnr(img, img_rec)
                
                ratios_plot.append(actual_r)
                psnrs_plot.append(p_val)
                data_summary.append({
                    '影像類型': name,
                    'Patch': f'{p}x{p}',
                    '目標比例': tr,
                    '實際比例': actual_r,
                    'PSNR': p_val
                })
        
        ax.plot(ratios_plot, psnrs_plot, 'o-', color=colors_map_comp[p], label=f'Patch {p}x{p}')"""

display_old = """plt.suptitle('四張不同特徵影像的 Patch SVD 效能比較', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()"""

display_new = """plt.suptitle('四張不同特徵影像的 Patch SVD 效能比較', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

df_summary = pd.DataFrame(data_summary)
styled_df_summary = (df_summary.style.pipe(apply_report_theme)
    .format({'實際比例': '{:.1f}x', 'PSNR': '{:.2f}'})
    .background_gradient(subset=['PSNR'], cmap='Blues')
    .set_caption("四張影像不同 Patch Size 比較")
)
display(styled_df_summary)"""

replaced = False
for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        src = "".join(cell["source"])
        if old_str in src:
            src = src.replace(old_str, new_str)
            src = src.replace(display_old, display_new)
            lines = src.split("\n")
            new_source = []
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    new_source.append(line + "\n")
                else:
                    if line:
                        new_source.append(line)
            cell["source"] = new_source
            replaced = True
            break

print("Replaced:", replaced)

with open("Homework/SML_Work2_411278018.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

