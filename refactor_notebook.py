import json

def read_nb(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_nb(nb, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

nb = read_nb("Homework/SML_Work2_411278018.ipynb")

# 1. Add apply_report_theme to setup cell
theme_code = """
import pandas as pd

def apply_report_theme(styler):
    \"\"\"自訂的報告表格基礎樣式\"\"\"
    return (styler
        .hide(axis="index")
        .set_properties(**{
            'text-align': 'center',
            'border': '1px solid #e0e0e0',
            'padding': '8px'
        })
        .set_table_styles([{
            'selector': 'th',
            'props': 'background-color: #f4f4f4; color: #333333; font-weight: bold; text-align: center; border-bottom: 2px solid #333333;'
        }])
    )
"""

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "setup_beautiful_plotting()" in source:
            if "apply_report_theme" not in source:
                cell["source"].insert(0, theme_code)
            break

# Helpers
def replace_source(nb, old, new):
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])
            if old in src:
                src = src.replace(old, new)
                lines = src.split("\n")
                new_source = []
                for i, line in enumerate(lines):
                    if i < len(lines) - 1:
                        new_source.append(line + "\n")
                    else:
                        if line:
                            new_source.append(line)
                cell["source"] = new_source
                return True
    return False

# Replacements
replacement_cell_7_old = """# 摘要表格
print(f"\\n{'='*55}")
print(f"{'奇異值能量摘要':^40}")
print(f"{'='*55}")
print(f"{'門檻':>6} | {'q（所需成分）':>12} | {'累積能量 %':>10} | {'壓縮比':>8}")
print(f"{'-'*55}")
for t in thresholds:
    k = q_thresholds[t]
    ratio = (m * n) / (k * (m + n + 1))
    print(f"  {int(t*100):>3}%  | {k:>12} | {t*100:>9.1f}% | {ratio:>6.1f}x")
print(f"{'='*55}")
print(f"影像尺寸：{m}×{n}，奇異值總數：{len(s)}")"""

replacement_cell_7_new = """# 摘要表格
data_7 = []
for t in thresholds:
    k = q_thresholds[t]
    ratio = (m * n) / (k * (m + n + 1))
    data_7.append({
        '門檻': f"{int(t*100)}%",
        'q（所需成分）': k,
        '累積能量 %': t,
        '壓縮比': ratio
    })
df_7 = pd.DataFrame(data_7)
styled_df_7 = (df_7.style.pipe(apply_report_theme)
    .format({'累積能量 %': '{:.1%}', '壓縮比': '{:.1f}x'})
    .set_caption(f"奇異值能量摘要 (影像尺寸：{m}×{n}，奇異值總數：{len(s)})")
)
display(styled_df_7)"""

replacement_cell_10_old = """print(f"\\n{'='*62}")
print(f"{'SVD rank-q 重建品質摘要':^50}")
print(f"{'='*62}")
print(f"{'q':>5} | {'壓縮比':>8} | {'PSNR (dB)':>10} | {'SSIM':>8} | {'儲存數值數':>12}")
print(f"{'-'*72}")

for idx, q in enumerate(q_values):
    A_q = svd_reconstruct(U, s, Vt, q)
    A_q_clipped = img_finalize(A_q)
    ratio = (m * n) / (q * (m + n + 1))
    p_val = psnr(A, A_q_clipped)
    s_val = ssim_metric(A, A_q_clipped)
    stored = q * (m + n + 1)

    axes[idx].imshow(A_q_clipped, cmap='gray', vmin=0, vmax=255)
    axes[idx].set_title(f'q={q}, r={ratio:.1f}x\\nPSNR={p_val:.1f}dB, SSIM={s_val:.3f}', fontsize=9)
    axes[idx].axis('off')
    print(f"  {q:>3} | {ratio:>7.1f}x | {p_val:>9.2f} | {s_val:>8.3f} | {stored:>12,}")

print(f"{'='*62}")
print(f"原始儲存量：{m*n:,} 像素")"""

replacement_cell_10_new = """data_10 = []
for idx, q in enumerate(q_values):
    A_q = svd_reconstruct(U, s, Vt, q)
    A_q_clipped = img_finalize(A_q)
    ratio = (m * n) / (q * (m + n + 1))
    p_val = psnr(A, A_q_clipped)
    s_val = ssim_metric(A, A_q_clipped)
    stored = q * (m + n + 1)

    axes[idx].imshow(A_q_clipped, cmap='gray', vmin=0, vmax=255)
    axes[idx].set_title(f'q={q}, r={ratio:.1f}x\\nPSNR={p_val:.1f}dB, SSIM={s_val:.3f}', fontsize=9)
    axes[idx].axis('off')
    data_10.append({
        'q': q,
        '壓縮比': ratio,
        'PSNR (dB)': p_val,
        'SSIM': s_val,
        '儲存數值數': stored
    })

df_10 = pd.DataFrame(data_10)
styled_df_10 = (df_10.style.pipe(apply_report_theme)
    .format({'壓縮比': '{:.1f}x', 'PSNR (dB)': '{:.2f}', 'SSIM': '{:.3f}', '儲存數值數': '{:,}'})
    .background_gradient(subset=['PSNR (dB)'], cmap='Blues')
    .set_caption(f"SVD rank-q 重建品質摘要 (原始儲存量：{m*n:,} 像素)")
)
display(styled_df_10)"""

replacement_cell_26_old = """# 示範：展示不同 patch_size 下達到相同壓縮比所需的 q
demo_ratio = 10.0
print(f"\\n目標壓縮比 {demo_ratio}x 所需的 q 值：")
print(f"{'patch_size':>12} | {'q':>6} | {'實際壓縮比':>10} | {'N_p':>8} | {'p²':>6}")
print("-" * 55)
for p in [1, 4, 8, 16, 32]:
    if m % p != 0 or n % p != 0:
        continue
    n_patches = (m // p) * (n // p)
    # 找最大 q 使得壓縮比 >= demo_ratio
    max_q_possible = min(n_patches, p * p)
    best_q = 0
    for q_try in range(1, max_q_possible + 1):
        if patch_compression_ratio(m, n, p, q_try) >= demo_ratio:
            best_q = q_try
        else:
            break
    if best_q > 0:
        actual_r = patch_compression_ratio(m, n, p, best_q)
        print(f"  {p:>3}×{p:<3}      | {best_q:>6} | {actual_r:>9.2f}x | {n_patches:>8} | {p*p:>6}")"""

replacement_cell_26_new = """# 示範：展示不同 patch_size 下達到相同壓縮比所需的 q
demo_ratio = 10.0
data_26 = []
for p in [1, 4, 8, 16, 32]:
    if m % p != 0 or n % p != 0:
        continue
    n_patches = (m // p) * (n // p)
    # 找最大 q 使得壓縮比 >= demo_ratio
    max_q_possible = min(n_patches, p * p)
    best_q = 0
    for q_try in range(1, max_q_possible + 1):
        if patch_compression_ratio(m, n, p, q_try) >= demo_ratio:
            best_q = q_try
        else:
            break
    if best_q > 0:
        actual_r = patch_compression_ratio(m, n, p, best_q)
        data_26.append({
            'patch_size': f"{p}×{p}",
            'q': best_q,
            '實際壓縮比': actual_r,
            'N_p': n_patches,
            'p²': p*p
        })

df_26 = pd.DataFrame(data_26)
styled_df_26 = (df_26.style.pipe(apply_report_theme)
    .format({'實際壓縮比': '{:.2f}x'})
    .set_caption(f"目標壓縮比 {demo_ratio}x 所需的 q 值")
)
display(styled_df_26)"""

replacement_cell_28_old = """# 印出 PSNR 表格
print(f"\\n{'='*72}")
print(f"{'Patch SVD 對照實驗：PSNR (dB)':^72}")
print(f"{'='*72}")
header = f"{'Patch size':>12} | " + " | ".join([f"{'r≈'+str(r)+'x':>12}" for r in target_ratios])
print(header)
print("-" * 72)
for p in patch_sizes:
    row = f"    {p:>2}×{p:<2}     | "
    for r in target_ratios:
        if (p, r) in results:
            res = results[(p, r)]
            row += f"  {res['psnr']:>6.2f}dB   | "
        else:
            row += f"{'N/A':>12} | "
    print(row)
print(f"{'='*72}")

# 印出實際使用的 q 值
print(f"\\n{'='*72}")
print(f"{'各組合使用的 q 值':^72}")
print(f"{'='*72}")
header2 = f"{'Patch size':>12} | " + " | ".join([f"{'r≈'+str(r)+'x':>12}" for r in target_ratios])
print(header2)
print("-" * 72)
for p in patch_sizes:
    row = f"    {p:>2}×{p:<2}     | "
    for r in target_ratios:
        if (p, r) in results:
            res = results[(p, r)]
            row += f"  q={res['q']:>3}({res['actual_ratio']:.1f}x) | "
        else:
            row += f"{'N/A':>12} | "
    print(row)
print(f"{'='*72}")"""

replacement_cell_28_new = """# PSNR 表格
data_28_psnr = []
for p in patch_sizes:
    row_data = {'Patch size': f"{p}×{p}"}
    for r in target_ratios:
        if (p, r) in results:
            row_data[f"r≈{r}x"] = results[(p, r)]['psnr']
        else:
            row_data[f"r≈{r}x"] = None
    data_28_psnr.append(row_data)

df_28_psnr = pd.DataFrame(data_28_psnr)
styled_df_28_psnr = (df_28_psnr.style.pipe(apply_report_theme)
    .format(na_rep='N/A', precision=2)
    .highlight_max(axis=0, subset=[f"r≈{r}x" for r in target_ratios], 
                   props='background-color: #d4edda; color: #155724; font-weight: bold;')
    .set_caption("Patch SVD 對照實驗：PSNR (dB)")
)
display(styled_df_28_psnr)

# 實際使用的 q 值表格
data_28_q = []
for p in patch_sizes:
    row_data = {'Patch size': f"{p}×{p}"}
    for r in target_ratios:
        if (p, r) in results:
            res = results[(p, r)]
            row_data[f"r≈{r}x"] = f"q={res['q']} ({res['actual_ratio']:.1f}x)"
        else:
            row_data[f"r≈{r}x"] = 'N/A'
    data_28_q.append(row_data)

df_28_q = pd.DataFrame(data_28_q)
styled_df_28_q = (df_28_q.style.pipe(apply_report_theme)
    .set_caption("各組合使用的 q 值")
)
display(styled_df_28_q)"""

replacement_cell_33_old = """print(f"\\n{'='*72}")
print(f"{'Patch Size 定量分析摘要':^55}")
print(f"{'='*72}")
print(f"{'Patch Size':>12} | {'歸一化熵 (SVE)':>15} | {'門檻秩佔比 (99%)':>18} | 備注")
print(f"{'-'*72}")
for i, p in enumerate(p_list):
    note = "（數學必然，不具比較意義）" if p == 1 else ""
    print(f"  {p:>2}×{p:<2}      | {sve_vals[i]:>15.4f} | {threshold_rank_ratios[i]:>18.2%} | {note}")
print(f"{'='*72}")"""

replacement_cell_33_new = """data_33 = []
for i, p in enumerate(p_list):
    note = "（數學必然，不具比較意義）" if p == 1 else ""
    data_33.append({
        'Patch Size': f"{p}×{p}",
        '歸一化熵 (SVE)': sve_vals[i],
        '門檻秩佔比 (99%)': threshold_rank_ratios[i],
        '備注': note
    })

df_33 = pd.DataFrame(data_33)
styled_df_33 = (df_33.style.pipe(apply_report_theme)
    .format({'歸一化熵 (SVE)': '{:.4f}', '門檻秩佔比 (99%)': '{:.2%}'})
    .set_caption("Patch Size 定量分析摘要")
)
display(styled_df_33)"""

replacement_cell_51_old = """print(f"\\n{'='*52}")
print(f"{'人臉資料能量摘要':^40}")
print(f"{'='*52}")
for t in thresholds_f:
    q_k = q_f[t]
    print(f"  累積 {int(t*100):>3}% 能量需要 q = {q_k:>3} 個特徵向量")
print(f"{'='*52}")
print(f"  總奇異值數：{len(s_f)}")
print(f"  前 10 個奇異值佔總能量比例：{energy_ratio_f[9]*100:.1f}%")"""

replacement_cell_51_new = """data_51 = []
for t in thresholds_f:
    q_k = q_f[t]
    data_51.append({
        '累積能量門檻': f"{int(t*100)}%",
        '所需 q 個數 (特徵向量)': q_k
    })

df_51 = pd.DataFrame(data_51)
styled_df_51 = (df_51.style.pipe(apply_report_theme)
    .set_caption(f"人臉資料能量摘要 (總奇異值數：{len(s_f)}，前 10 個奇異值佔總能量比例：{energy_ratio_f[9]:.1%})")
)
display(styled_df_51)"""

replacement_cell_56_old = """print(f"\\n{'='*75}")
print(f"{'人臉重建品質詳細摘要 (PSNR + SSIM)':^70}")
print(f"{'='*75}")
print(f"{'q':>5} | {'平均 PSNR':>10} | {'平均 SSIM':>12} | {'min PSNR':>8} | {'min SSIM':>8} | {'備注'}")
print(f"{'-'*75}")
for stat_p, stat_s in zip(psnr_stats, ssim_stats):
    q = stat_p['q']
    note = " ← 平均達標" if q == q_30dB else ""
    if stat_p['min'] >= 30 and note == "":
        note = " ← 全部達標"
    elif stat_p['min'] < 30 and stat_p['mean'] >= 30:
        note += " (仍有受試者 < 30dB)"
    print(f"  {q:>3} | {stat_p['mean']:>9.2f} | {stat_s['mean']:>12.4f} | {stat_p['min']:>8.2f} | {stat_s['min']:>8.4f} | {note}")
print(f"{'='*75}")
if q_30dB:
    print(f"\\n結論：達到平均 PSNR ≥ 30dB 需要 q = {q_30dB}。")
    print(f"但觀察分佈可知，在 q={q_30dB} 時最小值僅為 {next(stat['min'] for stat in psnr_stats if stat['q']==q_30dB):.2f}dB，")
    print(f"若要求『所有』受試者重建品質皆達 30dB，則建議 q 應提高至更高數值。")"""

replacement_cell_56_new = """data_56 = []
for stat_p, stat_s in zip(psnr_stats, ssim_stats):
    q = stat_p['q']
    note = " ← 平均達標" if q == q_30dB else ""
    if stat_p['min'] >= 30 and note == "":
        note = " ← 全部達標"
    elif stat_p['min'] < 30 and stat_p['mean'] >= 30:
        note += " (仍有受試者 < 30dB)"
    
    data_56.append({
        'q': q,
        '平均 PSNR': stat_p['mean'],
        '平均 SSIM': stat_s['mean'],
        'min PSNR': stat_p['min'],
        'min SSIM': stat_s['min'],
        '備注': note
    })

df_56 = pd.DataFrame(data_56)
styled_df_56 = (df_56.style.pipe(apply_report_theme)
    .format({'平均 PSNR': '{:.2f}', '平均 SSIM': '{:.4f}', 'min PSNR': '{:.2f}', 'min SSIM': '{:.4f}'})
    .background_gradient(subset=['平均 PSNR', '平均 SSIM'], cmap='Blues')
    .set_caption("人臉重建品質詳細摘要 (PSNR + SSIM)")
)
display(styled_df_56)

if q_30dB:
    print(f"\\n結論：達到平均 PSNR ≥ 30dB 需要 q = {q_30dB}。")
    print(f"但觀察分佈可知，在 q={q_30dB} 時最小值僅為 {next(stat['min'] for stat in psnr_stats if stat['q']==q_30dB):.2f}dB，")
    print(f"若要求『所有』受試者重建品質皆達 30dB，則建議 q 應提高至更高數值。")"""

replacement_cell_62_old = """# 6. 輸出表格
print(f"\\n{'='*40}")
print(f"{'1-NN 辨識實驗摘要':^30}")
print(f"{'='*40}")
print(f"  q 值 | 準確率 (%)")
print(f"{'-'*40}")
for q, acc in zip(q_values_recog, accuracies):
    print(f"  {q:>3}  | {acc:>6.1f}%")
print(f"{'='*40}")
print(f"準確率首次達 90% 的最小 q：{q_90}")
print(f"準確率首次達 95% 的最小 q：{q_95}")"""

replacement_cell_62_new = """# 6. 輸出表格
data_62 = []
for q, acc in zip(q_values_recog, accuracies):
    data_62.append({
        'q 值': q,
        '準確率': acc / 100.0
    })

df_62 = pd.DataFrame(data_62)
styled_df_62 = (df_62.style.pipe(apply_report_theme)
    .format({'準確率': '{:.1%}'})
    .highlight_max(subset=['準確率'], props='background-color: #d4edda; color: #155724; font-weight: bold;')
    .set_caption("1-NN 辨識實驗摘要")
)
display(styled_df_62)

print(f"準確率首次達 90% 的最小 q：{q_90}")
print(f"準確率首次達 95% 的最小 q：{q_95}")"""

replacement_cell_36_old = """print(f"\\n{'='*75}")
print(f"{'影像前處理效應：人臉 vs 幾何紋理':^70}")
print(f"{'='*75}")
print(f"{'影像類型':<25} | {'Patch':<6} | {'目標比例':<8} | {'實際比例':<8} | {'PSNR':<8}")
print("-" * 75)
for name, p_sizes in zip(["Olivetti Face (1st)", "Ascent (Geometric)"], [patch_sizes_faces, patch_sizes_ascent]):
    if name == "Olivetti Face (1st)":
        res_dict = results_faces
    else:
        res_dict = results_ascent
        
    for p in p_sizes:
        for tr in target_ratios_extra:
            if (p, tr) in res_dict:
                actual_r = res_dict[(p, tr)]['actual_ratio']
                p_val = res_dict[(p, tr)]['psnr']
                print(f"{name:<25} | {p:>2}x{p:<2} | {tr:>8} | {actual_r:>8.1f} | {p_val:>8.2f}")
print(f"{'='*75}")"""

replacement_cell_36_new = """data_36 = []
for name, p_sizes in zip(["Olivetti Face (1st)", "Ascent (Geometric)"], [patch_sizes_faces, patch_sizes_ascent]):
    if name == "Olivetti Face (1st)":
        res_dict = results_faces
    else:
        res_dict = results_ascent
        
    for p in p_sizes:
        for tr in target_ratios_extra:
            if (p, tr) in res_dict:
                data_36.append({
                    '影像類型': name,
                    'Patch': f"{p}×{p}",
                    '目標比例': tr,
                    '實際比例': res_dict[(p, tr)]['actual_ratio'],
                    'PSNR': res_dict[(p, tr)]['psnr']
                })

df_36 = pd.DataFrame(data_36)
styled_df_36 = (df_36.style.pipe(apply_report_theme)
    .format({'實際比例': '{:.1f}x', 'PSNR': '{:.2f}'})
    .background_gradient(subset=['PSNR'], cmap='Blues')
    .set_caption("影像前處理效應：人臉 vs 幾何紋理")
)
display(styled_df_36)"""

print("Replacing 7:", replace_source(nb, replacement_cell_7_old, replacement_cell_7_new))
print("Replacing 10:", replace_source(nb, replacement_cell_10_old, replacement_cell_10_new))
print("Replacing 26:", replace_source(nb, replacement_cell_26_old, replacement_cell_26_new))
print("Replacing 28:", replace_source(nb, replacement_cell_28_old, replacement_cell_28_new))
print("Replacing 33:", replace_source(nb, replacement_cell_33_old, replacement_cell_33_new))
print("Replacing 36:", replace_source(nb, replacement_cell_36_old, replacement_cell_36_new))
print("Replacing 51:", replace_source(nb, replacement_cell_51_old, replacement_cell_51_new))
print("Replacing 56:", replace_source(nb, replacement_cell_56_old, replacement_cell_56_new))
print("Replacing 62:", replace_source(nb, replacement_cell_62_old, replacement_cell_62_new))

write_nb(nb, "Homework/SML_Work2_411278018.ipynb")

print("Done updating notebook.")

