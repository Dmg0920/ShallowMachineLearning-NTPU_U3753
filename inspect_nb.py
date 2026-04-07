import json

with open("Homework/SML_Work2_411278018.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "apply_report_theme" not in source and ("print(" in source and "摘要" in source or "print(" in source and "各組合使用的 q 值" in source or "print(f\"\\n目標壓縮比" in source):
            print(f"--- Cell {i} ---")
            print(source)

