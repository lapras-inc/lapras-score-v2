FROM mcr.microsoft.com/devcontainers/base:bookworm

WORKDIR /workspace

# Install UV globally in /usr/local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh

COPY ./pyproject.toml ./pyproject.toml
COPY ./uv.lock ./uv.lock

CMD ["uv", "run", "-m", "examples.calculate_e_score_v2_from_rank_info_example"]
