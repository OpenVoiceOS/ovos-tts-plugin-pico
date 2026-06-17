FROM ubuntu:24.04

ENV TERM=linux
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    git python3 python3-dev python3-venv python3-pip \
    build-essential curl \
    libttspico0 libttspico-utils && \
  rm -rf /var/lib/apt/lists/*

# Use a venv so pip installs are not blocked by PEP 668 (externally-managed-environment).
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir ovos-tts-server

COPY . /tmp/ovos-tts-plugin-pico
RUN pip install --no-cache-dir /tmp/ovos-tts-plugin-pico

ENTRYPOINT ovos-tts-server --engine ovos-tts-plugin-pico
