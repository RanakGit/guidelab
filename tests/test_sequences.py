import pytest

from guidelab.sequences import clean_sequence, reverse_complement


def test_clean_sequence():
    assert clean_sequence(" atgc ") == "ATGC"


def test_reverse_complement_basic():
    assert reverse_complement("ATGC") == "GCAT"


def test_reverse_complement_keeps_n():
    assert reverse_complement("ANT") == "ANT"


def test_reverse_complement_empty():
    assert reverse_complement("") == ""


def test_clean_removes_whitespace():
    assert clean_sequence("AC GT\n\tAA") == "ACGTAA"


def test_clean_rejects_invalid_letters():
    with pytest.raises(ValueError):
        clean_sequence("ACGX")


def test_reverse_complement_lowercase():
    assert reverse_complement("atgc") == "GCAT"
