import numpy as np

from guidelab.sequences import clean_sequence

GUIDE_LENGTH = 20
_ROW = {"A": 0, "C": 1, "G": 2, "T": 3}


def one_hot_encode(seq, length=GUIDE_LENGTH):
    """Encode a DNA sequence as a 4 x len(seq) grid of 0s and 1s.

    Rows are A, C, G, T. An N becomes an all-zero column.
    Raises ValueError if the length differs from `length`
    (pass length=None to allow any length).
    """
    seq = clean_sequence(seq)
    if length is not None and len(seq) != length:
        raise ValueError(f"Expected {length} letters, got {len(seq)}")

    x = np.zeros((4, len(seq)), dtype=np.float32)
    for col, base in enumerate(seq):
        if base in _ROW:          # N is not in _ROW, so its column stays zero
            x[_ROW[base], col] = 1
    return x