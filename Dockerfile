# SVOX Pico served through ovos-tts-server's ElevenLabs-compatible API. A
# self-contained, fully offline image: any client that speaks the
# ovos-tts-server / ElevenLabs API can hit it, and it can be A/B-tested against
# other ovos-tts-server voices (phoonnx, edge-tts, ...) by pointing at a
# different port.
#
# pico2wave ships in Ubuntu's libttspico-utils package (not in python:3.11-slim's
# debian base), so this image is built on ubuntu:24.04 with a venv to sidestep
# PEP 668 (externally-managed-environment).
FROM ubuntu:24.04

ENV TERM=linux
ENV DEBIAN_FRONTEND=noninteractive

# libttspico0 + libttspico-utils provide the pico2wave binary the plugin shells out to.
RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 python3-venv python3-pip \
        libttspico0 libttspico-utils \
    && rm -rf /var/lib/apt/lists/*

# venv so pip installs are not blocked by PEP 668.
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . /app

# the plugin + the OVOS TTS server. setuptools<81 keeps ovos-plugin-manager's
# pkg_resources usage working. ovos-tts-server>=1.13.5a1's alpha floor lets pip
# resolve the prerelease without --pre (pico already emits WAV, no transcode needed).
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "setuptools<81" "." "ovos-tts-server>=1.13.5a1"

# Default voice/language, overridable with the PICO_VOICE build arg. Valid values:
# de-DE, en-GB, en-US, es-ES, fr-FR, it-IT.
ARG PICO_VOICE=en-US
RUN useradd -m -u 1000 ovos \
    && mkdir -p /home/ovos/.config/mycroft \
    && printf '{\n  "tts": {\n    "module": "ovos-tts-plugin-pico",\n    "ovos-tts-plugin-pico": {\n      "voice": "%s"\n    }\n  }\n}\n' "${PICO_VOICE}" \
        > /home/ovos/.config/mycroft/mycroft.conf \
    && chown -R 1000:1000 /home/ovos/.config
USER 1000

EXPOSE 9666
ENTRYPOINT ["ovos-tts-server", "--engine", "ovos-tts-plugin-pico", \
            "--host", "0.0.0.0", "--port", "9666", "--cache"]
