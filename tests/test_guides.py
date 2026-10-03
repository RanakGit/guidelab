from guidelab.guides import find_guides


def test_single_hit():
    seq = "A" * 20 + "TGG"
    assert find_guides(seq) == [("A" * 20, 0, "+")]
