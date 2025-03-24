from gtts import gTTS # type: ignore
from googletrans import Translator # type: ignore
import base64

LANGUAGES = [
    ('Bengali', 'bn'),
    ('Gujarati', 'gu'),
    ('Hindi', 'hi'),
    ('Kannada', 'kn'),
    ('Malayalam', 'ml'),
    ('Marathi', 'mr'),
    ('Nepali', 'ne'),
    ('Punjabi', 'pa'),
    ('Telugu', 'te'),
    ('Urdu', 'ur'),
    ('Arabic', 'ar'),
    ('English', 'en'),
    ('Tamil', 'ta'),
    ('French', 'fr'),
    ('German', 'de'),
    ('Italian', 'it'),
    ('Japanese', 'ja'),
    ('Korean', 'ko'),
    ('Russian', 'ru'),
    ('Spanish', 'es'),
    ('Chinese', 'zh-CN'),
    ('Morse Code', 'mc')
]

translator = Translator()


def getLanguages():
    return LANGUAGES


def getTranslated(lang_code, text):
    translated_text = translator.translate(text, dest=lang_code).text
    translated_audio_bytes = b''.join(
        [i for i in gTTS(translated_text, lang=lang_code).stream()])
    return {'audio': base64.b64encode(translated_audio_bytes).decode('utf-8'), 'result': translated_text, 'lang': [i[0] for i in LANGUAGES if i[1] == lang_code]}
