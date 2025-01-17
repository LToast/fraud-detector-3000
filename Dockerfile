# Docker multi-stage building, as recommended by https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry
FROM python:3.12-slim-bookworm as curl-stage

# Install curl ; remove apt cache to reduce image size
RUN apt-get -y update && apt-get -y install curl  && rm -rf /var/lib/apt/lists/*


FROM curl-stage as uv-requirements-stage

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app

RUN uv sync --frozen

# Copy API files
COPY src/api ./src/api

# Add and set a non-root user
RUN useradd appuser && chown -R appuser /app && chown -R appuser /root/.local
USER appuser

# Start FastAPI
CMD uv run uvicorn src.api.main:app --host 0.0.0.0 --port 80

# Healthcheck
HEALTHCHECK --interval=10s --timeout=1s --retries=3 CMD curl --fail http://localhost/health || exit 1
