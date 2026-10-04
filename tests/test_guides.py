from guidelab.guides import find_guides


def test_single_hit():
    seq = "A" * 20 + "TGG"
    assert find_guides(seq) == [("A" * 20, 0, "+")]


def test_no_pam():
    seq = "A" * 30
    assert find_guides(seq) == []


def test_too_short():
    seq = "A" * 20 + "GG"   # 22 letters: a PAM-looking ending but no room for the N
    assert find_guides(seq) == []


def test_pam_n_can_be_any_base():
    assert find_guides("A" * 20 + "AGG") == [("A" * 20, 0, "+")]
    assert find_guides("A" * 20 + "CGG") == [("A" * 20, 0, "+")]
    assert find_guides("A" * 20 + "GGG") == [("A" * 20, 0, "+")]

def test_overlapping_hits():
    seq = "A" * 21 + "GGG"   # 24 letters, G at positions 21, 22, 23
    assert find_guides(seq) == [("A" * 20, 0, "+"), ("A" * 20, 1, "+")]

def test_guide_letters_are_exact():
    guide = "ACGT" * 5              # 20 varied letters
    assert find_guides(guide + "TGG") == [(guide, 0, "+")]    