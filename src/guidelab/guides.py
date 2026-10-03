def find_guides(seq):
    hits = []
    for i in range(len(seq) - 22):          # how many valid start positions? (len 23 -> 1, len 24 -> 2)
        guide = seq[i:i + 20]
        pam = seq[i + 20:i + 23]
        if pam[-2:] == "GG":       # are the last two letters of pam "GG"? which slice?
            hits.append((guide, i, "+"))
    return hits