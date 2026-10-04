import numpy as np
import pytest

from guidelab.features import one_hot_encode


def test_one_hot_shape():
    assert one_hot_encode("A" * 20).shape == (4, 20)


def test_one_hot_values():
    x = one_hot_encode("ACGT" + "A" * 16)
    assert x[0, 0] == 1 and x[1, 1] == 1 and x[2, 2] == 1 and x[3, 3] == 1
    assert x.sum() == 20          # exactly one 1 per position


def test_one_hot_n_is_all_zeros():
    x = one_hot_encode("N" + "A" * 19)
    assert x[:, 0].sum() == 0     # the N column is all zeros
    assert x.sum() == 19          # the other 19 positions each have one 1


def test_one_hot_wrong_length():
    with pytest.raises(ValueError):
        one_hot_encode("ACGT")


def test_one_hot_lowercase_matches_uppercase():
    assert np.array_equal(one_hot_encode("a" * 20), one_hot_encode("A" * 20))


def test_one_hot_rejects_invalid_letters():
    with pytest.raises(ValueError):
        one_hot_encode("X" + "A" * 19)