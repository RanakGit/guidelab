from guidelab.guides import find_guides


def test_single_hit():
    seq = "A" * 20 + "TGG"
    assert find_guides(seq) == [("A" * 20, 0, "+")]


def test_no_pam():
    ...   # a 30-letter sequence with no "GG" anywhere -> []


def test_too_short():
    ...   # a sequence of 22 letters -> []


def test_pam_n_can_be_any_base():
    ...   # three sequences, 20 letters + "AGG", "CGG", "GGG"; each should return one hit


def test_overlapping_hits():
    ...   # length 24, with hits at positions 0 and 1; expect two tuples, in order