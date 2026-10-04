import numpy as np
import pytest

from guidelab.features import gc_content, one_hot_encode


def test_one_hot_shape():
    assert one_hot_encode("A" * 20).shape == (4, 20)


def test_one_hot_values():
    x = one_hot_encode("ACGT" + "A" * 16)
    assert x[0, 0] == 1 and x[1, 1] == 1 and x[2, 2] == 1 and x[3, 3] == 1
    assert x.sum() == 20  # exactly one 1 per position


def test_one_hot_n_is_all_zeros():
    x = one_hot_encode("N" + "A" * 19)
    assert x[:, 0].sum() == 0  # the N column is all zeros
    assert x.sum() == 19  # the other 19 positions each have one 1


def test_one_hot_wrong_length():
    with pytest.raises(ValueError):
        one_hot_encode("ACGT")


def test_one_hot_lowercase_matches_uppercase():
    assert np.array_equal(one_hot_encode("a" * 20), one_hot_encode("A" * 20))


def test_one_hot_rejects_invalid_letters():
    with pytest.raises(ValueError):
        one_hot_encode("X" + "A" * 19)


def test_gc_content_half():
    assert gc_content("GCAT" * 5) == 0.5


def test_gc_content_all_gc():
    assert gc_content("G" * 10 + "C" * 10) == 1.0


def test_gc_content_all_at():
    assert gc_content("A" * 20) == 0.0


def test_gc_content_lowercase():
    assert gc_content("gcat" * 5) == 0.5


def test_gc_content_empty_raises():
    with pytest.raises(ValueError):
        gc_content("")


def test_gc_content_with_n():
    assert gc_content("GCNN") == 0.5  # N counts toward the length
