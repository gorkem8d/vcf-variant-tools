import os
import pytest
from vcf_variant_tools.overlap import parse_gff_transcripts

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@pytest.fixture
def transcripts():
    """Parsed transcripts from the test GFF3."""
    path = os.path.join(DATA_DIR, "test_transcripts.gff3")
    with open(path) as f:
        return parse_gff_transcripts(f.readlines())

@pytest.fixture
def vcf_lines():
    """Non-header lines from the test VCF file."""
    path = os.path.join(DATA_DIR, "test_variants.vcf")
    with open(path) as f:
        return [line.strip() for line in f if not line.startswith("#")]