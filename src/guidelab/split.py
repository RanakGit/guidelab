import numpy as np


def split_by_gene(df, test_fraction=0.2, seed=0):
    """Split a table into train and test sets so no gene appears in both.

    df needs a "gene" column. Whole genes go to one side, chosen by a seeded
    shuffle of the sorted gene list, so the result does not depend on row order.
    Returns (train_df, test_df).
    """
    genes = sorted(df["gene"].unique())
    rng = np.random.default_rng(seed)
    shuffled = rng.permutation(genes)
    n_test = max(1, round(len(genes) * test_fraction))
    test_genes = set(shuffled[:n_test])
    is_test = df["gene"].isin(test_genes)
    return df[~is_test].reset_index(drop=True), df[is_test].reset_index(drop=True)
