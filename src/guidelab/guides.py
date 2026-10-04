from guidelab.sequences import clean_sequence, reverse_complement


def _scan(seq):
    """Scan one strand. Yield (guide, index) for every 20-mer followed by NGG."""
    for i in range(len(seq) - 22):  # 20 + 3 = 23 letters needed
        guide = seq[i : i + 20]
        pam = seq[i + 20 : i + 23]
        if pam[1:] == "GG":  # N can be anything; last two letters must be GG
            yield guide, i


def find_guides(seq):
    """Find guides on both strands.

    Returns (guide, start, strand) tuples, start being 0-based in the original
    sequence. Forward-strand hits come first, then reverse-strand hits in the
    order found (so their start positions descend).
    """
    seq = clean_sequence(seq)
    L = len(seq)
    hits = [(guide, i, "+") for guide, i in _scan(seq)]
    rc = reverse_complement(seq)
    hits += [(guide, L - 20 - j, "-") for guide, j in _scan(rc)]
    return hits
