import typing
from aiogram.types import InlineKeyboardMarkup
from aiogram_faq.types import PageStorage, PageConfig, PagePattern, KeyboardConfig


class Faq:
    __faqs = {}

    def __init__(self,
                 page_configs: typing.Iterable[PageConfig],
                 page_pattern: PagePattern,
                 keyboard_config: KeyboardConfig,
                 use_images: bool = False):

        if keyboard_config.button_content in page_pattern.compatible_keyboards:
            self._id: int = len(self.__faqs) + 1
            self._storage: PageStorage = PageStorage(
                page_pattern=page_pattern,
                page_configs=page_configs,
                image_is_required=use_images
            )
            self._keyboard_config: KeyboardConfig = keyboard_config
            self._filter_text: str = ''
            self._use_images: bool = use_images
            self.__faqs[self._id] = self
        else:
            raise TypeError('Page pattern is not compatible with keyboard buttons content!')

    @property
    def use_images(self) -> bool:
        return self._use_images

    @property
    def storage(self) -> PageStorage:
        return self._storage

    @property
    def id(self) -> int:
        return self._id

    @property
    def filter_text(self) -> str:
        return self._filter_text

    def get_keyboard(self, selected_page_id: int) -> InlineKeyboardMarkup:
        return self._keyboard_config.build_keyboard(
            pages=self._storage.pages,
            faq_id=self._id,
            selected_page_id=selected_page_id
        )

    @classmethod
    def get_faq(cls, faq_id: int):
        return cls.__faqs[faq_id]

    @classmethod
    def get_faqs(cls) -> list:
        return [cls.__faqs[key] for key in cls.__faqs]

    def register(self, filter_text: str):
        self._filter_text = filter_text

__all__ = ['Faq']
