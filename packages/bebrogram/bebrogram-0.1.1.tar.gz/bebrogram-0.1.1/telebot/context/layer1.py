from .layer0 import ContextLayer0
from ..objects import Message, User, Chat, CallbackQuery


class ContextLayer1(ContextLayer0):

    @property
    def message(self) -> Message | None:
        """ Message | ChannelPost | CallbackQuery.message """
        value = None

        if update := self.update:
            value = update.message or update.channel_post

            if value is None:
                if callback_query := self.callback_query:
                    value = callback_query.message

        return value

    @property
    def callback_query(self) -> CallbackQuery | None:
        """ CallbackQuery """
        value = None

        if update := self.update:
            value = update.callback_query

        return value

    @property
    def chat(self) -> Chat | None:
        """ Message.chat | ChannelPost.chat | CallbackQuery.chat """

        value = None

        if message := self.message:
            value = message.chat

        return value

    @property
    def user(self) -> User | None:
        """ Message.user | CallbackQuery.user """
        value = None

        if update := self.update:
            if message := update.message:
                value = message.from_user
            elif callback_query := update.callback_query:
                value = callback_query.from_user

        return value

