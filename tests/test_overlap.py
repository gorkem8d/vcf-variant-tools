
from vcf_variant_tools.overlap import overlaps, parse_gff_transcripts, find_overlapping_transcripts

def test_clear_overlap():
    assert overlaps(10, 20, 15, 25) is True

def test_no_overlap():
    assert overlaps(10, 20, 21, 30) is False

def test_touching_boundary():
    # share only 1 pos
    assert overlaps(10, 20, 20, 30) is True

def test_contained():
    # one interval is fully inside the other
    assert overlaps(10, 50, 20, 30) is True

def test_symmetry():
    # overlap (A,B) should equal overlap (B, A)
    assert overlaps(10, 20, 15, 25) == overlaps(15,25,10,20)
    assert overlaps(10, 20, 30, 40) == overlaps(30, 40, 10, 20)

def test_parse_gff(transcripts):
    """Should find 4 transcripts in our test file."""
    assert len(transcripts) == 4

def test_snv_overlaps_one(transcripts):
    """SNV at chr1:100 should hit ENST00000001 (50-250) only."""
    result = find_overlapping_transcripts("chr1", 100, 100, transcripts)
    assert result == ["ENST00000001"]

def test_variant_overlaps_two(transcripts):
    """Position chr1:500 is where ENST00000002 (350-550) and ENST00000003 (500-800) meet."""
    result = find_overlapping_transcripts("chr1", 500, 500, transcripts)
    assert "ENST00000002" in result
    assert "ENST00000003" in result
    assert len(result) == 2

def test_no_overlap(transcripts):
    """chr1:900 is beyond all chr1 transcripts."""
    result = find_overlapping_transcripts("chr1", 900, 900, transcripts)
    assert result == []

def test_wrong_chromosome(transcripts):
    """chr5 has no transcripts at all."""
    result = find_overlapping_transcripts("chr5", 100, 200, transcripts)
    assert result == []