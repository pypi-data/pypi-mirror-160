import abc
import typing
import functools

from pyrogram.client import Client
from pyrogram.filters import Filter
from pyrogram.handlers.handler import Handler
from pyrogram.handlers import MessageHandler

from pyrogram.types import Update

import asyncio

loop = asyncio.get_event_loop()

class MetaStore(abc.ABC):
    """
    pyrostep steps store interface.

    See: `~pyrostep.steps.change_store`
    """
    @abc.abstractmethod
    def __setitem__(
        self, key: int, value: typing.Union[typing.Callable[..., typing.Coroutine], asyncio.Future]
    ) -> None:
        """
        stores the key and value.
        """
        pass

    @abc.abstractmethod
    def __getitem__(self, key: int) -> typing.Union[typing.Callable[..., typing.Coroutine], asyncio.Future]:
        """
        returns the stored value, or raise KeyError.
        """
        pass
    
    @abc.abstractmethod
    def __delitem__(self, key: int) -> None:
        """
        removes the stored key and value.
        """
        pass

    @abc.abstractmethod
    def clear(self) -> None:
        """
        removes all stored keys and values.
        """
        pass

root = dict() # type: MetaStore

def change_store(store: MetaStore) -> None:
    """
    configs root key-value store.

    Example::

        from pyrostep.steps import MetaStore, change_store

        class SimpleStore(MetaStore):

            STORE = dict()

            def __setitem__(self, key, value):
                self.DICT[key] = value
            
            def __getitem__(self, key):
                return self.DICT[key]
            
            def clear(self):
                self.DICT.clear()
        
        change_store( SimpleStore() )
    """
    global root

    root = store

async def _listen_function(_c, _u) -> None:
    """
    listen decorator to listen. 
    """
    fn = None

    try:
        fn = root[_u.from_user.id]
    except (KeyError, AttributeError):
        
        try:
            fn = root[_u.chat.id]
        except (KeyError, AttributeError):
            pass

    if not (fn is None):
        if isinstance(fn, asyncio.Future):
            fn.set_result(_u)
            return
        
        await fn(_c, _u)

def listen(app: Client, handler: Handler = MessageHandler, filters: Filter = None, group: int = 0):
    """
    listens a client by handlers.

    *Use it after all handlers/decorators.

    supported handlers:
        - `MessageHandler`
        - `CallbackQueryHandler`
        - `ChatJoinRequestHandler`
        - `ChatMemberUpdatedHandler`
        - `ChosenInlineResultHandler`
        - `EditedMessageHandler`
        - `InlineQueryHandler`
    
    Example::

        app = Client(...)
        # ...
        listen(app)
    """
    app.add_handler(handler(_listen_function, filters), group)

def listen_on_the_side(cls):
    """
    listens a client by decorator.

    supported decorators:
        - `on_message`
        - `on_callback_query`
        - `on_chat_join_request`
        - `on_chat_member_updated`
        - `on_chosen_inline_result`
        - `on_edited_message`
        - `on_inline_query`
    
    Example::

        app = Client(...)
        
        @app.on_message()
        @listen_on_the_side
        async def message_handler(client, message):
            ...
    """
    @functools.wraps(cls)
    async def wrapper(_c, _u):
        try:
            fn = root[_u.from_user.id]
        except (KeyError, AttributeError):
            return await cls(_c, _u)
        else:
            return await fn(_c, _u)
    
    return wrapper

def register_next_step(user_id: int, _next) -> None:
    """
    register_next_step sets next step for user.

    Parameters:
        user_id (``int``):
            user numeric id.
        
        _next (``(Client, pyrogram.types.Update) -> Any``):
            next step handler.
    
    Example::
        
        async def step1(client, msg):
            # code ...
            register_next_step(msg.from_user.id, step2)
        
        async def step2(client, msg):
            # code ...
    """
    root[user_id] = _next

def unregister_steps(user_id: int) -> None:
    """
    removes all user step's.

    Parameters:
        user_id (``int``):
            user numeric id.
    """
    try:
        del root[user_id]
    except KeyError:
        pass

async def ask(app: Client, _next, chat_id: int, text: str, user_id:int=None, *args, **kwargs) -> None:
    """
    it is shorthand for app.send_message(chat_id, text, *args, **kwargs); register_next_step(chat_id, _next)
    """
    await app.send_message(chat_id, text, *args, **kwargs)
    register_next_step(user_id or chat_id, _next)

async def ask_wait(
    app: Client, chat_id: int, text: str, timeout:float=None, user_id:int=None, *args, **kwargs
) -> Update:
    """
    ask from user and wait for answer.

    Parameter:
        app (`Client`):
            client.
        
        chat_id (`int`):
            chat id.
        
        text (`str`):
            text to send.
        
        timeout (`float | None`):
            time to wait for answer.
        
        user_id (`int | None`):
            wait for user answer if not None, wait for all users in chat answer otherwise.
        
        *args, **kwargs (`Any`):
            Client.send_message parameters.
    
    Example::

        # wait for answer in pv
        answer = await ask_wait(app, 102393493, "What is your name?")

        # wait for answer in group ( all users )
        answer = await ask_wait(app, -102892437, "Whoever answers first is the winner")

        # wait for answer in group ( only one user )
        answer = await ask_wait(app, -102892437, "What is your name?", user_id=506286293)
    """
    await app.send_message(chat_id, text, *args, **kwargs)

    fn = loop.create_future()

    fn.add_done_callback(
        lambda _: unregister_steps(user_id or chat_id)
    )

    root[chat_id] = fn

    return await asyncio.wait_for(fn, timeout)

def clear() -> None:
    """
    removes all user's step's.
    """
    root.clear()
