# AGENTS.md — ovos-tts-plugin-pico

OVOS TTS plugin wrapping the offline PicoTTS engine (`pico2wave` / `pico-tts` / `nanotts` CLI binaries).

## Setup

```bash
pip install .
```

Requires a PicoTTS binary on PATH. On Debian/Pi:

```bash
sudo apt-get install libttspico0 libttspico-utils
```

The plugin probes for `nanotts`, then `pico2wave`, then `pico-tts` (in that priority order) and raises `RuntimeError` at init if none is found.

## Test

No unit tests for the TTS logic. The only test is a license compliance check:

```bash
pip install git+https://github.com/NeonJarbas/lichecker pytest pytest-timeout pytest-cov
pytest test/license_tests.py
```

## Lint/Typecheck

None configured.

## Layout

- `ovos_tts_plugin_pico/__init__.py` — single-module implementation. `PicoTTS(TTS)` (synthesis), `PicoTTSValidator(TTSValidator)` (lang + binary checks), `PicoTTSPluginConfig` (per-lang config dict), and `get_voice_from_lang()` (lang code -> Pico voice).
- `test/license_tests.py` — dependency license allowlist check.
- `Dockerfile` — packages the plugin as an `ovos-tts-server` HTTP service.
- `setup.py` — packaging; entry points below.
- `pico.wav` — sample output artifact (committed).

Entry-point groups:
- `mycroft.plugin.tts` -> `ovos_tts_plugin_pico:PicoTTS`
- `mycroft.plugin.tts.config` -> `ovos_tts_plugin_pico:PicoTTSPluginConfig`

Supported voices: `de-DE`, `en-GB`, `en-US`, `es-ES`, `fr-FR`, `it-IT`.

## Conventions (Org hard rules)

- Branches: work on `dev`, stable is `master`. NEVER use `main`.
- Never edit `version.py` / `version` — gh-automations bumps semver from conventional-commit prefixes (`feat:` / `fix:` / `feat!:`).
- New repos are private by default; do not make a source repo public without asking.
- Commit identity: `JarbasAi <jarbasai@mailfence.com>`.
- Reference `OpenVoiceOS/gh-automations` reusable workflows at `@dev`.
- No Neon / `neon-*` references.
- No meta-commentary (no history, dates, "design mistake" narration); describe current state only.
- CI is provided by `OpenVoiceOS/gh-automations`.

## Gotchas

- `setup.py` pins `install_requires=['ovos-plugin-manager>=0.0.1a12']` but `requirements.txt` says `ovos-plugin-manager>=2.1.0,<2.2.0`; setup.py does not read requirements.txt, so the installed pin is the stale alpha. Keep them in sync via setup.py.
- Three backends with differing output handling: `pico2wave` and `nanotts` write WAV directly; `pico-tts` emits raw PCM_U8 over stdout and is wrapped into a 16 kHz mono 16-bit WAV in `get_picotts`.
- `get_voice_from_lang` returns `None` for unsupported langs; `get_tts` falls back to `self.voice` in that case.
- Speed/pitch are not supported (nanotts TODO).
