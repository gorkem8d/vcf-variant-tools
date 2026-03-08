# Before running tests, install pytest: pip install pytest

from vcf_variant_tools.normalizer import normalize_variant
import pytest
import os

@pytest.mark.parametrize(
    "pos, ref, alt, expected_pos, expected_ref, expected_alt",
    [
        # SNV — nothing to strip
        (100, "A", "T", 100, "A", "T"),
        # Deletion with left anchor
        (100, "ATCG", "A", 100, "ATCG", "A"),
        # Deletion with extra prefix to strip
        (100, "ATCGA", "AT", 101, "TCGA", "T"),
        # Suffix strip only
        (50, "AGTCC", "ACC", 50, "AGT", "A"),
        # Prefix strip reduces to SNV
        (10, "AATG", "AACG", 12, "T", "C"),
        # Insertion — nothing to strip
        (100, "A", "ATCG", 100, "A", "ATCG"),
    ],
    ids=[
        "snv",
        "deletion-left-anchor",
        "deletion-extra-prefix",
        "suffix-strip-only",
        "prefix-strip-to-snv",
        "insertion",
    ],
)
def test_normalization_cases(pos, ref, alt, expected_pos, expected_ref, expected_alt):
    """Test normalization across a range of variant types."""
    result_pos, result_ref, result_alt = normalize_variant(pos, ref, alt)
    assert result_pos == expected_pos
    assert result_ref == expected_ref
    assert result_alt == expected_alt

