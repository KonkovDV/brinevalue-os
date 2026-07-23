FROM python:3.12-slim

WORKDIR /app

# Install as root, then drop privileges for runtime.
COPY pyproject.toml README.md LICENSE ./
COPY brinevalue ./brinevalue
RUN pip install --no-cache-dir -e ".[api,dashboard,excel]" \
    && useradd --create-home --uid 10001 --shell /usr/sbin/nologin brinevalue \
    && chown -R brinevalue:brinevalue /app

USER brinevalue

EXPOSE 8000 8501
CMD ["python", "-m", "brinevalue.cli", "demo", "--index", "0"]
