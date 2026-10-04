import pandas as pd

from guidelab.split import split_by_gene


def _toy(n_genes=20, per_gene=5):
    rows = [
        (f"b{g:04d}", f"guide{g}_{i}") for g in range(n_genes) for i in range(per_gene)
    ]
    return pd.DataFrame(rows, columns=["gene", "guide"])


def test_no_gene_on_both_sides():
    train, test = split_by_gene(_toy())
    assert set(train["gene"]).isdisjoint(set(test["gene"]))


def test_every_row_used_once():
    df = _toy()
    train, test = split_by_gene(df)
    assert len(train) + len(test) == len(df)


def test_same_seed_same_split():
    a_train, _ = split_by_gene(_toy(), seed=1)
    b_train, _ = split_by_gene(_toy(), seed=1)
    assert list(a_train["guide"]) == list(b_train["guide"])


def test_test_fraction_roughly_respected():
    _, test = split_by_gene(_toy(n_genes=20), test_fraction=0.25)
    assert test["gene"].nunique() == 5


def test_row_order_does_not_change_split():
    df = _toy()
    shuffled = df.sample(frac=1, random_state=3)
    _, test_a = split_by_gene(df, seed=5)
    _, test_b = split_by_gene(shuffled, seed=5)
    assert set(test_a["gene"]) == set(test_b["gene"])
