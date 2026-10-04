VALID_BASES = "ACGTN"
_COMPLEMENT = str.maketrans("ACGTN", "TGCAN")


def clean_sequence(seq):
    """Remove all whitespace, uppercase, and reject invalid letters."""
    cleaned = "".join(seq.split()).upper()
    bad = set(cleaned) - set(VALID_BASES)
    if bad:  # when should this raise?
        raise ValueError(f"Invalid letters: {sorted(bad)}")
    return cleaned


def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    seq = clean_sequence(seq)
    return seq[::-1].translate(_COMPLEMENT)
