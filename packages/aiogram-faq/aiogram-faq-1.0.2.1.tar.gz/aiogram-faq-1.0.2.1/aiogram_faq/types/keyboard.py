import typing
from aiogram_faq.types.button_content import ButtonContent
from aiogram_faq.types.page import Page
from aiogram_faq.utils import border_value, replace_many
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardConfig:

    def __init__(self,
                 width: int,
                 mark_selected: bool,
                 button_content: ButtonContent,
                 url_buttons: list[list[InlineKeyboardButton]] = None):
        self._width = border_value(width, 1, 8, 1)
        self._mark_selected = mark_selected
        self._button_content = button_content
        self._url_buttons = [] if url_buttons is None else url_buttons

    def build_keyboard(self,
                       pages: typing.Iterable[Page],
                       faq_id: int,
                       selected_page_id: int) -> InlineKeyboardMarkup:
        keyboard = []
        row = []
        i = 0
        for page in pages:
            page: Page
            if i >= self._width:
                i = 0
                keyboard.append(row)
                row = []
            i += 1
            row.append(self._create_button(
                page=page,
                faq_id=faq_id,
                is_selected=selected_page_id == page.id))
        keyboard.append(row)
        if len(self._url_buttons) > 0:
            keyboard.extend(self._url_buttons)
        keyboard.append([InlineKeyboardButton('✖ Закрыть', callback_data='close_faq')])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)

    def _create_button(self,
                       page: Page,
                       faq_id: int,
                       is_selected: bool) -> InlineKeyboardButton:
        text = replace_many(
            self._button_content.value,
            (ButtonContent.PageId.value, page.id),
            (ButtonContent.PageTitle.value, page.title),
            ('<b>', ''), ('<code>', ''), ('<i>', ''), ('<u>', ''), ('<s>', ''),
            ('</b>', ''), ('</code>', ''), ('</i>', ''), ('</u>', ''), ('</s>', '')
        )
        if is_selected and self._mark_selected:
            text = '• ' + text + ' •'
        callback_data = 'faq_{faq_id}_open_page_{page_id}'.format(faq_id=faq_id, page_id=page.id)
        return InlineKeyboardButton(text, callback_data=callback_data)

    @property
    def width(self) -> int:
        return self._width

    @property
    def mark_selected(self) -> bool:
        return self._mark_selected

    @property
    def button_content(self) -> ButtonContent:
        return self._button_content




__all__ = ['ButtonContent', 'KeyboardConfig']