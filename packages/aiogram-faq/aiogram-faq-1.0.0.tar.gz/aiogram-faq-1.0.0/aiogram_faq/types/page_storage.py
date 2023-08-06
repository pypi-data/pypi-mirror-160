import typing
from aiogram_faq.types.page import Page, PageConfig, PagePattern


class PageStorage:

    def __init__(self,
                 page_configs: typing.Iterable[PageConfig],
                 page_pattern: PagePattern,
                 image_is_required: bool):
        self._pages = {}
        self._image_is_required = image_is_required
        for page_config in page_configs:
            if isinstance(page_config, PageConfig):
                page_id = len(self._pages) + 1
                image = None
                if image_is_required:
                    image = Page.get_image(page_config.image_path)
                    if image is None:
                        raise ValueError('Image required, but is not exist! Add correct image path to page_config!')
                self._pages[page_id] = Page(
                    id=page_id,
                    pattern=page_pattern,
                    config=page_config,
                    image=image
                )

    @property
    def pages(self) -> list[Page]:
        return [self._pages[index] for index in self._pages]

    def get_page(self, page_id: int):
        return self._pages[page_id]

__all__ = ['PageStorage']