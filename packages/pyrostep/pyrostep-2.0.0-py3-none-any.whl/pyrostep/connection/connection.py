import functools
from pyrogram.connection import Connection
from pyrogram.session import Session

import logging

from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.errors import RPCError, AuthKeyDuplicated
from pyrogram.raw.all import layer

import typing

log = logging.getLogger(__name__)

def connection_max_retries(max_retries:int=None) -> typing.Optional[int]:
    """
    Change connection max retries. (default 3)

    retries message:
        Unable to connect due to network issues: ...

    Return:
        returns MAX_RETRIES if max_retries is None
    """
    if not isinstance(max_retries, int):
        return Connection.MAX_RETRIES

    Connection.MAX_RETRIES = max_retries

def invoke_max_retries(max_retries:int=None) -> typing.Optional[int]:
    """
    Change invoke max retries. (default 5)

    retries message:
        [...] Waiting for ... seconds before continuing (required by "...")
    
    Return:
        returns MAX_RETRIES if max_retries is None
    """
    if not isinstance(max_retries, int):
        return Session.MAX_RETRIES

    Session.MAX_RETRIES = max_retries

def session_start_timeout(timeout: int = None) -> typing.Optional[int]:
    """
    Change start timeout. (default 1)

    Return:
        returns START_TIMEOUT if timeout is None. 
    """
    if not isinstance(timeout, int):
        return Session.START_TIMEOUT

    Session.START_TIMEOUT = timeout

def session_max_retries(max_retries: int, mode: int = 3) -> None:
    """
    Change session max retries.

    retries message:
        Connection failed! Trying again...
    
    What is mode? TCP Connection mode.

    TCP Modes:
        0: TCPFull
        1: TCPAbridged
        2: TCPIntermediate
        3: TCPAbridgedO
        4: TCPIntermediateO
    """

    @functools.wraps(Session.start)
    async def _session_start(self):
        for i in range(max_retries):
            self.connection = Connection(
                self.dc_id,
                self.test_mode,
                self.client.ipv6,
                self.client.proxy,
                self.is_media,
                mode=mode,
            )
            try:
                await self.connection.connect()
                self.network_task = self.loop.create_task(self.network_worker())
                await self.send(raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT)
                if not self.is_cdn:
                    await self.send(
                        raw.functions.InvokeWithLayer(
                            layer=layer,
                            query=raw.functions.InitConnection(
                                api_id=await self.client.storage.api_id(),
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack="",
                                query=raw.functions.help.GetConfig(),
                            )
                        ),
                        timeout=self.START_TIMEOUT
                    )
                self.ping_task = self.loop.create_task(self.ping_worker())
                log.info(f"Session initialized: Layer {layer}")
                log.info(f"Device: {self.client.device_model} - {self.client.app_version}")
                log.info(f"System: {self.client.system_version} ({self.client.lang_code.upper()})")
            except AuthKeyDuplicated as e:
                await self.stop()
                raise e
            except (OSError, TimeoutError, RPCError) as e:
                await self.stop()
                if i == (max_retries-1):
                    raise e
            except Exception as e:
                await self.stop()
                raise e
            else:
                break
        
        self.is_connected.set()
        log.info("Session started")
    
    Session.start = _session_start
