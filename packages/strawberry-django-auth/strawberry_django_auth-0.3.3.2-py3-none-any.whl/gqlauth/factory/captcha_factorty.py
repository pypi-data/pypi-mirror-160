from base64 import b64encode
from dataclasses import dataclass
import io
from pathlib import Path
import sys

from PIL.Image import Image

from gqlauth.settings import gqlauth_settings as app_settings

from .create import ImageCaptcha

sys.path.append(str(Path(__file__).parent.parent.parent))
FONTS_PATH = str(Path(__file__).parent.joinpath("fonts"))


@dataclass
class CaptchaType:
    image: Image
    text: str

    def as_base64(self):
        bytes_array = io.BytesIO()
        self.image.save(bytes_array, format="PNG")
        return b64encode(bytes_array.getvalue())

    def show(self):
        self.image.show()


def get_image(text):
    image = ImageCaptcha(
        width=300,
        height=150,
        heb_fonts=[FONTS_PATH + "/stam.ttf"],
        fonts=[FONTS_PATH + "/OpenSans-Semibold.ttf"],
    )
    image = image.generate_image(text)
    return image


def generate_text() -> str:
    return app_settings.CAPTCHA_TEXT_FACTORY()


def generate_captcha_text():
    text = generate_text()
    image = get_image(text)
    return CaptchaType(image=image, text=text)
