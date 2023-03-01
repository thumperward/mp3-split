FROM mcr.microsoft.com/devcontainers/base:debian

# TODO: use python versions and not linux cli tools
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install --no-install-recommends \
  python3-pip \
  mp3info \
  ffmpeg

# TODO: eyed3 cli requires non-venv version of pylast
RUN pip install \
  poetry \
  pre-commit \
  detect-secrets
