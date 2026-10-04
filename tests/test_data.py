import pandas as pd

from guidelab.data import load_screen


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
