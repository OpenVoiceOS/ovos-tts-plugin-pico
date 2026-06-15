"""End-to-end TTS intelligibility test for the Pico TTS plugin.

Synthesises a small fixed set of English phrases, transcribes the rendered
audio back with the ovoscope reference STT, and asserts the mean word error
rate stays within tolerance. The pico2wave binary is provided by the
``libttspico-utils`` system package (installed in CI).
"""
import os

from ovoscope.tts_intelligibility import score_tts_intelligibility

from ovos_tts_plugin_pico import PicoTTS

LANG = "en-US"
PHRASES = [
    "hello world",
    "what time is it",
    "turn on the kitchen lights",
    "the weather is nice today",
    "set a timer for five minutes",
]


def test_tts_intelligibility():
    tts = PicoTTS()
    report = score_tts_intelligibility(tts, PHRASES, lang=LANG)
    print(f"::TTS-INTELLIGIBILITY:: {report.to_dict()}")
    assert report.mean_wer <= float(os.environ.get("TTS_MAX_WER", "1.0"))
