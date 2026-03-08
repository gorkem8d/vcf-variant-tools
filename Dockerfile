FROM python:3.12-slim
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY vcf_variant_tools/ vcf_variant_tools/
COPY tests/ tests/

# Install the package with test dependencies
RUN pip install ".[dev]"

# Run tests during build — if tests fail, the image won't build
RUN pytest -v

# Default command
CMD ["python", "-m", "vcf_variant_tools"]

#open -a Docker
#docker build -t vcf-variant-tools .