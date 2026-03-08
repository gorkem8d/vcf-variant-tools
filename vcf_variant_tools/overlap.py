def parse_gff_transcripts(lines):
    """
    Parse transcript features from GFF3 lines.

    Args:
        lines: List of GFF3 lines (headers and comments are skipped).

    Returns:
        List of dictionaries, each with keys:
        transcript_id, chrom, start, end, strand.
    """
    transcripts = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        fields = line.split("\t")
        if len(fields) < 9:
            continue

        feature_type = fields[2]
        if feature_type != "transcript":
            continue

        # Parse attributes (9th column): ID=ENST001;gene_name=TP53
        attrs = {}
        for item in fields[8].split(";"):
            if "=" in item:
                key, value = item.strip().split("=", 1)
                attrs[key] = value

        transcripts.append({
            "transcript_id": attrs.get("ID", "unknown"),
            "chrom": fields[0],
            "start": int(fields[3]),
            "end": int(fields[4]),
            "strand": fields[6],
        })

    return transcripts


def overlaps(start1, end1, start2, end2):
    """
    Check whether two 1-based inclusive intervals overlap.

    Args:
        start1, end1: First interval.
        start2, end2: Second interval.

    Returns:
        True if the intervals share at least one position.
    """
    return start1 <= end2 and start2 <= end1


def find_overlapping_transcripts(chrom, start, end, transcripts):
    """
    Find all transcripts that overlap a genomic region.

    Args:
        chrom: Chromosome name.
        start: 1-based inclusive start position.
        end:   1-based inclusive end position.
        transcripts: List of transcript dicts from parse_gff_transcripts.

    Returns:
        List of transcript IDs that overlap the region.
    """
    results = []
    for t in transcripts:
        if t["chrom"] == chrom and overlaps(start, end, t["start"], t["end"]):
            results.append(t["transcript_id"])
    return sorted(results)
