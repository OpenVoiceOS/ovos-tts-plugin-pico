# TODO — ovos-tts-plugin-pico

## Open issues

- [ ] #12 Dependency Dashboard (Renovate)

## Gaps

- [ ] No unit tests for synthesis logic (only `test/license_tests.py`).
- [ ] CI uses legacy hand-rolled workflows, not `OpenVoiceOS/gh-automations` reusable workflows. Missing standard `build-tests`, `coverage`, `license-check`, `release_workflow`, `publish_stable`. Custom `dev2master.yml` should be replaced by the gh-automations release workflow.
- [ ] No `opm-check` workflow despite declaring `mycroft.plugin.tts` entry points.
- [ ] Migrate `setup.py` -> `pyproject.toml` (org standard packaging).
- [ ] `setup.py` `install_requires` pins `ovos-plugin-manager>=0.0.1a12` while `requirements.txt` pins `>=2.1.0,<2.2.0`; reconcile.
- [ ] Stale `setup.py` metadata: `description='pico tts plugin for mycroft'`, Python 2.x / 3.0-3.6 classifiers.
- [ ] Committed scratch artifacts: `ovos_tts_plugin_pico.egg-info/` and `pico.wav`.
- [ ] `license_tests.py` installs licheck from `NeonJarbas/lichecker` (Neon-org reference); prefer the org-standard license-check workflow.

## Code TODOs

- [ ] `ovos_tts_plugin_pico/__init__.py:31` — support speed and pitch for nanotts.
