"""The validator's two rejection paths, and the exception type of each.

Both raised a bare Exception until this was written. A bare Exception is
uncatchable in practice: a caller that wants to handle an unsupported
language has to catch Exception, which also swallows every programming
error in the same block. The types are asserted here so the next rewrite of
these messages cannot quietly widen them back.

The plugin loader (ovos_plugin_manager.tts) catches Exception around
validate() and re-raises, so it does not read the type. Nothing else in the
organisation matches on either the type or the message text, checked by
grep before the change.
"""
import unittest
from unittest.mock import patch

from ovos_tts_plugin_pico import PicoTTSValidator


class _FakeTTS:
    """The validator only reads tts.lang."""

    def __init__(self, lang):
        self.lang = lang


def _validator(lang):
    return PicoTTSValidator(_FakeTTS(lang))


class TestValidateLang(unittest.TestCase):
    def test_unsupported_language_raises_valueerror(self):
        with self.assertRaises(ValueError) as caught:
            _validator("ja-JP").validate_lang()
        self.assertIn("PicoTTS only supports", str(caught.exception))

    def test_a_supported_language_is_accepted(self):
        """The control. Without it a validator that rejected everything
        would pass the test above."""
        for lang in ("de-DE", "en-GB", "en-US", "es-ES", "fr-FR", "it-IT",
                     "en", "EN-gb", "it"):
            with self.subTest(lang=lang):
                self.assertIsNone(_validator(lang).validate_lang())


class TestValidateConnection(unittest.TestCase):
    def test_no_binary_raises_runtimeerror(self):
        with patch("ovos_tts_plugin_pico.find_executable", return_value=None), \
                self.assertRaises(RuntimeError) as caught:
            _validator("en-US").validate_connection()
        self.assertIn("PicoTTS is not installed", str(caught.exception))

    def test_any_one_binary_is_enough(self):
        """The control, and it also pins that the three names are checked
        as alternatives rather than all required."""
        for present in ("pico2wave", "pico-tts", "nanotts"):
            def found(n, p=present):
                return "/usr/bin/" + n if n == p else None

            with self.subTest(binary=present), \
                    patch("ovos_tts_plugin_pico.find_executable", found):
                self.assertIsNone(_validator("en-US").validate_connection())


if __name__ == "__main__":
    unittest.main()
