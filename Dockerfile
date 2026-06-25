FROM python:3.10-slim

# Create a non-root user
RUN useradd -m -s /bin/bash fortress

# Set working directory
WORKDIR /home/fortress/app

# Copy application files
COPY --chown=fortress:fortress . .

# Install dependencies
RUN pip install --no-cache-dir -e .

# Switch to non-root user
USER fortress

# Set entrypoint
ENTRYPOINT ["python", "-m", "credential_fortress.main"]
CMD ["--help"]
