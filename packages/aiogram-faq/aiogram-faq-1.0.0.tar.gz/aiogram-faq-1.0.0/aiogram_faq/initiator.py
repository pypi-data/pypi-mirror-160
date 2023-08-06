from enum import Enum

from aiogram.utils import exceptions

from aiogram_faq.faq import Faq
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State


class Update(Enum):
    Message = 0
    CallbackQuery = 1


class Initiator:

    __filter_alias__ = None
    __base_registered = False

    def __init__(self, update: Update, text: str, state: State = '*'):
        self.__update: Update = update
        self.__text: str = text
        self.__state: State = state
        self.__filter: dict = {self.__filter_alias__: self.__text}

    def __check(self, text: str) -> bool:
        return self.__text == text

    def register_handlers(self, faq: Faq, dispatcher: Dispatcher):
        faq.register(self.__text)
        if self.__update == Update.Message:
            dispatcher.register_message_handler(
                **self.__filter,
                callback=self._callback_on_message,
                state=self.__state
            )
        elif self.__update == Update.CallbackQuery:
            dispatcher.register_callback_query_handler(
                **self.__filter,
                callback=self._callback_on_call,
                state=self.__state
            )
        if not self.__base_registered:
            dispatcher.register_callback_query_handler(
                callback=self._callback_on_close_faq,
                text='close_faq'
            )
            dispatcher.register_callback_query_handler(
                callback=self._callback_on_open_page,
                regexp=r'faq_\d+_open_page_\d+'
            )
            self.__base_registered = True

    async def _callback_on_message(self, msg: types.Message, state: FSMContext):
        await state.finish()
        for faq in Faq.get_faqs():
            if self.__check(faq.filter_text):
                page = faq.storage.pages[0]
                if faq.use_images:
                    await msg.answer_photo(
                        photo=page.input_file,
                        caption=page.compiled,
                        reply_markup=faq.get_keyboard(1)
                    )
                else:
                    await msg.answer(
                        text=page.compiled,
                        reply_markup=faq.get_keyboard(1)
                    )
                break

    async def _callback_on_call(self, call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        for faq in Faq.get_faqs():
            if self.__check(faq.filter_text):
                page = faq.storage.pages[0]
                if faq.use_images:
                    await call.message.answer_photo(
                        photo=page.input_file,
                        caption=page.compiled,
                        reply_markup=faq.get_keyboard(1)
                    )
                else:
                    await call.message.answer(
                        text=page.compiled,
                        reply_markup=faq.get_keyboard(1)
                    )
                break

    @staticmethod
    async def _callback_on_close_faq(call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        await call.message.delete()

    @staticmethod
    async def _callback_on_open_page(call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        try:
            params = call.data.split('_')
            faq_id, page_id = int(params[1]), int(params[4])
            faq = Faq.get_faq(faq_id)
            page = faq.storage.get_page(page_id)

            if faq.use_images:
                await call.message.edit_media(
                    media=types.InputMediaPhoto(
                        media=page.input_file,
                        caption=page.compiled),
                    reply_markup=faq.get_keyboard(page_id)
                )
            else:
                await call.message.edit_text(
                    text=page.compiled,
                    reply_markup=faq.get_keyboard(page_id)
                )
        except exceptions.MessageNotModified:
            await call.answer(
                text='Вы уже итак на этой странице!',
                show_alert=True
            )


class InitiatorOnTextEquals(Initiator):
    __filter_alias__ = 'text'

    def __check(self, text: str) -> bool:
        return self.__text == text

class InitiatorOnTextContains(Initiator):
    __filter_alias__ = 'text_contains'

    def __check(self, text: str) -> bool:
        return self.__text in text

class InitiatorOnTextStartswith(Initiator):
    __filter_alias__ = 'text_startswith'

    def __check(self, text: str) -> bool:
        return self.__text.startswith(text)

class InitiatorOnTextEndswith(Initiator):
    __filter_alias__ = 'text_endswith'

    def __check(self, text: str) -> bool:
        return self.__text.endswith(text)


__all__ = [
    'Initiator', 'Update', 'InitiatorOnTextEquals', 'InitiatorOnTextContains', 'InitiatorOnTextStartswith',
    'InitiatorOnTextEndswith'
]