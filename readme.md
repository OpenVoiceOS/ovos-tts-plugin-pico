## Description

This is an OpenVoiceOS TTS plugin for [PicoTTS](https://github.com/naggety/picotts), a
fully offline text-to-speech engine.

## Install

```bash
pip install ovos-tts-plugin-pico
```

`pico2wave` must be available. On a Raspberry Pi, install it with:

```bash
apt-get install libttspico0
apt-get install libttspico-utils
```

You can also install it from [source](https://github.com/naggety/picotts).

## Configuration

```json
  "tts": {
    "module": "ovos-tts-plugin-pico"
 }
```

The voice corresponds to a language code. OVOS auto-detects it from the global config.

You can also set it explicitly to one of `"de-DE", "es-ES", "fr-FR", "it-IT", "en-US"`:

```json
  "tts": {
    "module": "ovos-tts-plugin-pico",
    "ovos-tts-plugin-pico": {
      "voice": "en-US"
    }
 }
```

## Docker (ovos-tts-server)

A container image runs the plugin as an
[`ovos-tts-server`](https://github.com/OpenVoiceOS/ovos-tts-server) (ElevenLabs-compatible
API). CI builds and pushes the image to GHCR on every push to `dev` or `master`:

```bash
docker run -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-pico:latest
curl "http://localhost:9666/synthesize/hello%20world?lang=en-US" --output hello.wav
```

The `PICO_VOICE` build arg bakes the served voice into the image (default `en-US`; valid
values `de-DE`, `en-GB`, `en-US`, `es-ES`, `fr-FR`, `it-IT`). Rebuild the image to change
it, for example:

```bash
docker build --build-arg PICO_VOICE=de-DE -t pico-tts .
```

See the bundled `docker-compose.yml`. Pico runs fully offline, so the container needs no
network access or API keys.

## Related projects

- [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager) loads this
  plugin through the `opm.tts` entry point.
- [ovos-tts-server](https://github.com/OpenVoiceOS/ovos-tts-server) serves this plugin
  over an HTTP API, and is what the bundled Docker image runs.

## License

Apache-2.0. See [LICENSE](LICENSE).
