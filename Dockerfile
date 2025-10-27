FROM agrigorev/zoomcamp-model:2025

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /code

COPY "pyproject.toml" "uv.lock" ".python-version" ./

RUN uv sync --locked

ENV PATH="/code/.venv/bin:$PATH"

COPY "predict.py" ./

EXPOSE 9696

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]