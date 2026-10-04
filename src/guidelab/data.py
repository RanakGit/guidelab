import pandas as pd

KEEP = {
    "sequence": "guide",
    "sequence_30nt": "context30",
    "geneid": "gene",
    "log2FC": "score",
}


def load_screen(path, screen, essential_coding_only=True):
    """Read one tab-separated CRISPRi screen file and return a clean table."""
    df = pd.read_csv(path, sep="\t")
    if essential_coding_only:
        df = df[
            (df["gene_essentiality"] == 1) & (df["coding_strand"] == 1)
        ]  # essential AND coding strand: two conditions
    df = df[df["sequence_30nt"].str.len() == 30]
    df = df.dropna(subset=["log2FC"])
    df = df.rename(columns=KEEP)[list(KEEP.values())]
    df["screen"] = screen
    return df.reset_index(drop=True)


def gene_residuals(df, min_guides=3):
    """Add a 'resid' column: each guide's score minus its gene's median score.

    Genes with fewer than min_guides guides are dropped, because a median of one
    or two values says almost nothing. The input table is not modified.
    """
    sizes = df.groupby("gene")["score"].transform("size")
    out = df[sizes >= min_guides].copy()  # keep genes with enough guides
    out["resid"] = out["score"] - out.groupby("gene")["score"].transform("median")
    return out.reset_index(drop=True)
