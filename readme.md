## Description

OpenVoiceOS TTS plugin for [PicoTTS](https://github.com/naggety/picotts)

## Install

```bash
pip install ovos-tts-plugin-pico
```

`pico2wave` needs to be available, in a pi this can be installed with

```bash
apt-get install libttspico0
apt-get install libttspico-utils
```

you can also install from [source](https://github.com/naggety/picotts)


## Configuration


```json
  "tts": {
    "module": "ovos-tts-plugin-pico"
 }
```

the Voice corresponds to a language code, it should be auto detected from global config

you can also set it explicitly to one of `"de-DE", "es-ES", "fr-FR", "it-IT", "en-US"`


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
API), built and pushed to GHCR by CI on every push to `dev`/`master`:

```bash
docker run -p 9666:9666 ghcr.io/openvoiceos/ovos-tts-plugin-pico:latest
curl "http://localhost:9666/synthesize/hello%20world?lang=en-US" --output hello.wav
```

The served voice is baked in via the `PICO_VOICE` build arg (default `en-US`; valid
values `de-DE`, `en-GB`, `en-US`, `es-ES`, `fr-FR`, `it-IT`); rebuild to change it, e.g.
`docker build --build-arg PICO_VOICE=de-DE -t pico-tts .`. See the bundled
`docker-compose.yml`. Pico runs fully offline — no network access or API keys needed.