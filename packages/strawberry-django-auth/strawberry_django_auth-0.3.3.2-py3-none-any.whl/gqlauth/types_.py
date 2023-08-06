from uuid import UUID

import strawberry
import strawberry_django

from gqlauth import models
from gqlauth.scalars import image


@strawberry_django.type(model=models.Captcha)
class CaptchaType:
    uuid: UUID

    @strawberry.field
    def image(self) -> image:
        return self.as_bytes()
