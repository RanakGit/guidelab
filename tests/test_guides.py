from guidelab.guides import find_guides
from guidelab.sequences import reverse_complement


def test_single_hit():
    seq = "A" * 20 + "TGG"
    assert find_guides(seq) == [("A" * 20, 0, "+")]


def test_no_pam():
    seq = "A" * 30
    assert find_guides(seq) == []


def test_too_short():
    seq = "A" * 20 + "GG"  # 22 letters: a PAM-looking ending but no room for the N
    assert find_guides(seq) == []


def test_pam_n_can_be_any_base():
    assert find_guides("A" * 20 + "AGG") == [("A" * 20, 0, "+")]
    assert find_guides("A" * 20 + "CGG") == [("A" * 20, 0, "+")]
    assert find_guides("A" * 20 + "GGG") == [("A" * 20, 0, "+")]


def test_overlapping_hits():
    seq = "A" * 21 + "GGG"  # 24 letters, G at positions 21, 22, 23
    assert find_guides(seq) == [("A" * 20, 0, "+"), ("A" * 20, 1, "+")]


def test_guide_letters_are_exact():
    guide = "ACGT" * 5  # 20 varied letters
    assert find_guides(guide + "TGG") == [(guide, 0, "+")]


def test_find_guides_accepts_lowercase():
    assert find_guides("a" * 20 + "tgg") == [("A" * 20, 0, "+")]


def test_reverse_strand_hit():
    seq = reverse_complement("A" * 20 + "TGG")  # "CCA" + "T" * 20
    assert find_guides(seq) == [("A" * 20, 3, "-")]


def test_reverse_strand_two_hits():
    seq = "C" + reverse_complement("A" * 20 + "TGG")  # 24 letters
    L = len(seq)
    assert find_guides(seq) == [
        ("A" * 20, L - 20 - 0, "-"),  # hit at j = 0 in the reverse complement
        ("A" * 19 + "T", L - 20 - 1, "-"),  # hit at j = 1
    ]
