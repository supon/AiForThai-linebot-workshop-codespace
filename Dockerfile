FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV TZ=Asia/Bangkok

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /workspace