FROM python:3.11-slim-bookworm AS build

COPY --from=ghcr.io/astral-sh/uv:0.5.12-python3.11-bookworm-slim /usr/local/bin/uv /bin/uv

COPY . /work
WORKDIR /work

RUN apt update && apt install -y build-essential libpq-dev
RUN uv sync --all-groups
RUN uv pip freeze > requirements.txt
RUN uv run pex . -o sample-api-app.pex -e main -r requirements.txt -D src

FROM python:3.11-slim-bookworm

COPY --from=build /work/sample-api-app.pex /sample-api-app.pex

CMD ["/sample-api-app.pex"]