import os
import wave
import tempfile
import unittest

from ovos_tts_plugin_pico import PicoTTS, get_voice_from_lang


class TestVoiceMapping(unittest.TestCase):
    def test_lang_to_voice(self):
        self.assertEqual(get_voice_from_lang("de-de"), "de-DE")
        self.assertEqual(get_voice_from_lang("es-es"), "es-ES")
        self.assertEqual(get_voice_from_lang("fr-fr"), "fr-FR")
        self.assertEqual(get_voice_from_lang("it-it"), "it-IT")
        self.assertEqual(get_voice_from_lang("en-us"), "en-US")
        self.assertEqual(get_voice_from_lang("en-gb"), "en-GB")
        self.assertEqual(get_voice_from_lang("en-uk"), "en-GB")


class TestPicoTTS(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tts = PicoTTS(config={"lang": "en-us"})

    def test_available_languages(self):
        langs = self.tts.available_languages
        self.assertIn("en", langs)
        self.assertIn("de", langs)

    def test_get_tts_creates_valid_wav(self):
        path = os.path.join(tempfile.mkdtemp(), "pico_out.wav")
        wav_file, _ = self.tts.get_tts("Hello world", path)
        self.assertTrue(os.path.isfile(wav_file))
        self.assertGreater(os.path.getsize(wav_file), 0)
        # ensure it is a parseable WAV with audio frames
        with wave.open(wav_file, "rb") as f:
            self.assertGreater(f.getnframes(), 0)
            self.assertGreater(f.getframerate(), 0)

    def test_get_tts_per_lang(self):
        path = os.path.join(tempfile.mkdtemp(), "pico_de.wav")
        wav_file, _ = self.tts.get_tts("Hallo Welt", path, lang="de-de")
        self.assertTrue(os.path.isfile(wav_file))
        self.assertGreater(os.path.getsize(wav_file), 0)


if __name__ == "__main__":
    unittest.main()
