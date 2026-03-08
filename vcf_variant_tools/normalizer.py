def normalize_variant(pos, ref, alt, chrom=None):
    """
    Normalize a VCF variant to its minimal, left-aligned representation.

    Args:
        pos:   1-based genomic position.
        ref:   Reference allele string.
        alt:   Alternate allele string.
        chrom: Optional chromosome name.

    Returns:
        Tuple of (pos, ref, alt) after normalization.

    Raises:
        ValueError: If ref or alt is empty, or pos < 1.
    """
    if not ref or not alt:
        raise ValueError(f"REF and ALT must be non-empty strings: ref={ref!r}, alt={alt!r}")
    if pos < 1:
        raise ValueError(f"POS must be >= 1, got {pos}")

    ref = list(ref.upper())
    alt = list(alt.upper())

    # Step 1: Strip common suffix (right-trim)
    while len(ref) > 1 and len(alt) > 1 and ref[-1] == alt[-1]:
        ref.pop()
        alt.pop()

    # Step 2: Strip common prefix (left-trim), adjusting position
    while len(ref) > 1 and len(alt) > 1 and ref[0] == alt[0]:
        ref.pop(0)
        alt.pop(0)
        pos += 1

    return pos, "".join(ref), "".join(alt)