import os
from dataclasses import dataclass
from io import BytesIO

from aiogram_faq.types.button_content import ButtonContent
from aiogram_faq.utils import replace_many
from aiogram import types

@dataclass
class PagePattern:
    body: str
    compatible_keyboards: tuple[ButtonContent]


@dataclass
class PageConfig:
    title: str
    content: str
    image_path: str = ''


class Page:
    def __init__(self,
                 id: int,
                 config: PageConfig,
                 pattern: PagePattern,
                 image: types.InputFile):
        self.id: int = id
        self.title: str = config.title
        self.content: str = config.content
        self.pattern: PagePattern = pattern
        self.image = image

    @property
    def compiled(self) -> str:
        return replace_many(self.pattern.body, ('<title>', self.title), ('<content>', self.content), ('<id>', self.id))

    @classmethod
    def get_image(cls, path: str) -> bytes:
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read()
        return None

    @property
    def input_file(self) -> types.InputFile:
        return types.InputFile(BytesIO(initial_bytes=self.image))


class PagePatterns:
    TitleContent = PagePattern('<title>\n\n<content>', (ButtonContent.PageTitle, ))
    IdTitleContent = PagePattern('<id> <title>\n\n<content>', (ButtonContent.PageId, ))


__all__ = ['Page', 'PageConfig', 'PagePattern', 'PagePatterns']