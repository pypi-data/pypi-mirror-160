from pyrogram.filters import create, Filter
from pyrogram.types import Message, Update
from pyrogram.client import Client
from ..shortcuts import validation_channels

import typing

#region ttl_message_filter
async def ttl_message_filter(_, __, m: Message) -> bool:
    return (m.photo and m.photo.ttl_seconds) or (m.video and m.video.ttl_seconds)

ttl_message = create(ttl_message_filter, name="ttl_message")
"""Filter ttl messages ( ttl photo message or ttl video message )."""
#endregion


#region video_sticker_filter
async def video_sticker_filter(_, __, m: Message) -> bool:
    return m.sticker and m.sticker.is_video

video_sticker = create(video_sticker_filter, name="video_sticker")
"""Filter video sticker messages."""
#endregion


#region entities_filter
async def entities_filter(_, __, m: Message) -> bool:
    return bool(m.entities or m.caption_entities)

entities = create(entities_filter, name="entities")
"""Filter messages include entities."""
#endregion


#region photo_size_filter
def photo_size(width: int, height: int) -> Filter:
    """
    Filter photo messages with width and height.
    
    Example::
        
        @app.on_message(photo_size(512, 512))
    """
    async def photo_size_filter(_, __, m: Message) -> bool:
        return m.photo and m.photo.width == width and m.photo.height == height

    return create(photo_size_filter, name="photo_size")
#endregion

#region chats_filter
def member_of_chats(
    channels: typing.Iterable[typing.Union[str, int]],
    invite_func: typing.Callable[[Client, int, typing.Iterable[typing.Union[int, str]]], typing.Coroutine] = None
) -> Filter:
    """
    Filter users who are members of chats.

    supported decorators:
        - `on_message`
        - `on_callback_query`
        - `on_chat_join_request`
        - `on_chat_member_updated`
        - `on_chosen_inline_result`
        - `on_edited_message`
        - `on_inline_query`

    Parameters:
        channels (`list[int | str]`):
            list of channels id or username.

        invite_func (`(Client, int, list[int | str]) -> None`, `optional`):
            validation_channels calls it when user not member of channels. (before return False)
    """
    async def member_of_chats_filter(_, app, update: Update) -> bool:
        try:
            return await validation_channels(app, update.from_user.id, channels, invite_func)
        except AttributeError:
            return False

    return create(member_of_chats_filter, name="member_of_chats")
#endregion
