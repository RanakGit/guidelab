import pandas as pd
from scipy.stats import spearmanr

from guidelab.data import load_screen

RAW = "data/raw/yu2024/"
screens = {
    "Cui": "E18_Cui.csv",
    "Rousset": "E75_Rousset.csv",
    "Wang": "Wang_dataset.csv",
}
d = {name: load_screen(RAW + f, name) for name, f in screens.items()}

for name, df in d.items():
    print(
        f"{name}: {len(df)} guides, {df['gene'].nunique()} genes, "
        f"median score {df['score'].median():.2f}"
    )

union = pd.concat(d.values()).drop_duplicates("guide")
print("unique guides across the three screens:", len(union))

m = d["Cui"].merge(d["Rousset"], on="guide", suffixes=("_cui", "_rou"))
rho = spearmanr(m["score_cui"], m["score_rou"])[0]
print(f"Cui vs Rousset on the same guides (n={len(m)}): Spearman = {rho:.3f}")

# Remove each gene's typical score, so only guide-to-guide differences remain
for name, df in d.items():
    df["resid"] = df["score"] - df.groupby("gene")["score"].transform("median")
m = d["Cui"].merge(d["Rousset"], on="guide", suffixes=("_cui", "_rou"))
rho_w = spearmanr(m["resid_cui"], m["resid_rou"])[0]
print(f"Within-gene Cui vs Rousset (n={len(m)}): Spearman = {rho_w:.3f}")
print("guides per gene (median):", d["Cui"].groupby("gene").size().median())
