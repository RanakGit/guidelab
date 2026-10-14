import pandas as pd
import pytest

from guidelab.data import build_dataset, gene_residuals, load_screen


def _make_file(tmp_path, rows):
    cols = [
        "sequence",
        "sequence_30nt",
        "log2FC",
        "geneid",
        "gene_essentiality",
        "coding_strand",
    ]
    path = tmp_path / "toy.csv"
    pd.DataFrame(rows, columns=cols).to_csv(path, sep="\t", index=False)
    return path


def _row(guide_letter, essential=1, coding=1, score=-2.0, gene="b0001"):
    guide = guide_letter * 20
    context = "C" * 4 + guide + "TGG" + "CCC"  # 4 + 20 + 3 + 3 = 30
    return (guide, context, score, gene, essential, coding)


def test_renames_columns(tmp_path):
    path = _make_file(tmp_path, [_row("A")])
    df = load_screen(path, "toy")
    assert list(df.columns) == ["guide", "context30", "gene", "score", "screen"]
    assert df.loc[0, "screen"] == "toy"


def test_drops_bad_context(tmp_path):
    bad = list(_row("C"))
    bad[1] = "ACG"  # a 3-letter context instead of 30
    path = _make_file(tmp_path, [_row("A"), tuple(bad)])
    df = load_screen(path, "toy")
    assert list(df["guide"]) == ["A" * 20]  # the good row survived


def test_essential_coding_filter(tmp_path):
    rows = [
        _row("A", essential=1, coding=1),
        _row("C", essential=0, coding=1),
        _row("G", essential=1, coding=0),
    ]
    path = _make_file(tmp_path, rows)
    assert list(load_screen(path, "toy")["guide"]) == ["A" * 20]
    assert len(load_screen(path, "toy", essential_coding_only=False)) == 3


def test_drops_missing_score(tmp_path):
    rows = [_row("A", score=-2.0), _row("C", score=float("nan"))]
    path = _make_file(tmp_path, rows)
    df = load_screen(path, "toy")
    assert list(df["guide"]) == ["A" * 20]


def test_gene_residuals_subtract_median():
    df = pd.DataFrame(
        {"gene": ["a"] * 4 + ["b"] * 3, "score": [-1, -2, -3, -4, -10, -20, -30]}
    )
    out = gene_residuals(df)
    # gene a median is -2.5, gene b median is -20
    assert list(out["resid"]) == [1.5, 0.5, -0.5, -1.5, 10.0, 0.0, -10.0]


def test_gene_residuals_does_not_modify_input():
    df = pd.DataFrame({"gene": ["a"] * 3, "score": [-1.0, -2.0, -3.0]})
    gene_residuals(df)
    assert "resid" not in df.columns


def test_gene_residuals_drops_small_genes():
    df = pd.DataFrame(
        {"gene": ["a"] * 4 + ["b"] * 2, "score": [-1, -2, -3, -4, -5, -6]}
    )
    out = gene_residuals(df, min_guides=3)
    assert set(out["gene"]) == {"a"}


def _screen(rows):
    """rows: list of (guide, gene, score) -> a table like load_screen returns."""
    df = pd.DataFrame(rows, columns=["guide", "gene", "score"])
    df["context30"] = "ctx_" + df["guide"]
    return df


def test_build_one_row_per_guide_and_scales_agree():
    s1 = _screen([("g1", "a", -1), ("g2", "a", -2), ("g3", "a", -3)])
    s2 = _screen([("g1", "a", -10), ("g2", "a", -20), ("g3", "a", -30)])  # 10x scale
    out = build_dataset({"x": s1, "y": s2})
    assert len(out) == 3
    assert list(out["n_screens"]) == [2, 2, 2]
    assert list(out["label"]) == pytest.approx([1.0, 0.0, -1.0])


def test_build_counts_screens_per_guide():
    s1 = _screen([("g1", "a", -1), ("g2", "a", -2), ("g3", "a", -3)])
    s2 = _screen([("g3", "a", -3), ("g4", "a", -4), ("g5", "a", -5)])
    out = build_dataset({"x": s1, "y": s2}).set_index("guide")
    assert len(out) == 5
    assert out.loc["g3", "n_screens"] == 2
    assert out.loc["g1", "n_screens"] == 1


def test_build_labels_have_unit_spread():
    s = _screen(
        [
            ("g1", "a", -1),
            ("g2", "a", -2),
            ("g3", "a", -3),
            ("g4", "b", -10),
            ("g5", "b", -20),
            ("g6", "b", -30),
        ]
    )
    out = build_dataset({"x": s})
    assert out["label"].std() == pytest.approx(1.0)


def test_build_label_ignores_screen_scale():
    base = _screen([("g1", "a", -1), ("g2", "a", -2), ("g3", "a", -3)])
    bigger = base.copy()
    bigger["score"] = bigger["score"] * 7
    out_a = build_dataset({"x": base})
    out_b = build_dataset({"x": bigger})
    assert out_a["label"].tolist() == pytest.approx(out_b["label"].tolist())
