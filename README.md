# vcf-variant-tools

Utilities for VCF variant normalization and transcript overlap detection — two core operations in variant effect prediction pipelines.

Built as a demonstration of bioinformatics software development practices including unit testing, containerization, and CI/CD.

## Features

**Variant Normalization** (`vcf_variant_tools.normalizer`)
- Parsimonious representation: strips common suffixes then prefixes
- Left-alignment following VCF 4.x specification
- Multi-allelic record splitting
- Variant type classification (SNV, insertion, deletion, MNV, complex)

**Transcript Overlap Detection** (`vcf_variant_tools.overlap`)
- GFF3 transcript parsing
- Interval-based overlap queries
- Chromosome-binned index for efficient batch lookups

## Installation

```bash
# From source
pip install -e ".[dev]"

# Or with Docker
docker build -t vcf-variant-tools .
```

## Usage

```python
from vcf_variant_tools import normalize_variant, find_overlapping_transcripts

# Normalize a variant
nv = normalize_variant(pos=100, ref="ATCGA", alt="AT", chrom="chr1")
print(f"{nv.chrom}:{nv.pos} {nv.ref}>{nv.alt} ({nv.variant_type})")
# chr1:101 TCGA>T (deletion)

# Parse transcripts and find overlaps
from vcf_variant_tools.overlap import parse_gff_transcripts, TranscriptIndex

with open("transcripts.gff3") as f:
    transcripts = parse_gff_transcripts(f.readlines())

index = TranscriptIndex(transcripts)
result = index.query("chr1", 101, 104)
print(result.transcript_ids)
```

### CLI

```bash
# Normalize a VCF file
python -m vcf_variant_tools normalize input.vcf

# Find transcript overlaps
python -m vcf_variant_tools overlap input.vcf transcripts.gff3
```

### Docker

```bash
docker build -t vcf-variant-tools .
docker run --rm -v $(pwd)/data:/data vcf-variant-tools normalize /data/input.vcf
```

## Testing

```bash
# Run tests
make test

# Run with coverage
make test-cov

# Run tests inside Docker
make docker-test
```

**Test suite:** 71 tests covering normalization edge cases, interval overlap logic, GFF3 parsing, multi-allelic splitting, and index consistency.

## Project Structure

```
vcf-variant-tools/
├── vcf_variant_tools/
│   ├── __init__.py
│   ├── __main__.py          # CLI entry point
│   ├── normalizer.py        # Variant normalization
│   └── overlap.py           # Transcript overlap detection
├── tests/
│   ├── conftest.py           # Shared fixtures
│   ├── test_normalizer.py    # 36 tests
│   ├── test_overlap.py       # 35 tests
│   └── data/
│       ├── test_variants.vcf
│       └── test_transcripts.gff3
├── Dockerfile                # Multi-stage build
├── Makefile                  # Dev automation
├── pyproject.toml            # Package config
└── .github/workflows/ci.yml  # GitHub Actions CI
```


