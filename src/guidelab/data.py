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
