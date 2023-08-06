# Pyrostep

[![Downloads](https://static.pepy.tech/personalized-badge/pyrostep?period=total&units=abbreviation&left_color=red&right_color=grey&left_text=Downloads)](https://pepy.tech/project/pyrostep) ![Python](https://img.shields.io/static/v1?label=Language&message=Python&color=blue&style=flat&logo=python) ![Pyrogram](https://img.shields.io/static/v1?label=Framework&message=Pyrogram&color=red&style=flat)

Pyrostep helps you to use pyrogram:
- step handling
- new filters may you need
- change connection timeout, retries, e.g.
- and other helper methods

> I tried to provide the best speed ...

1. [Install](#install)
2. [Usage](#usage)
    1. [Step handling](#step-handling)
    2. [New filters](#new-filters)
    3. [Connection](#connection)
    4. [Other](#other)
4. [TODO](#todo)

# Install
```bash
pip3 install -U pyrostep
```

# Usage

> **before learn, You should know that this library only works as async.**

## Step handling

import `pyrostep.steps` first:
```python
from pyrostep import steps
```

Now see simple example:
```python
@app.on_message(filters.command("start"))
async def step1(c, msg):
    await app.send_message(msg.chat.id, "what is your name?")
    steps.register_next_step(msg.from_user.id, step2)

async def step2(c, msg):
    await app.send_message(msg.chat.id, "your name is: %s" % msg.text)
    steps.unregister_steps(msg.from_user.id)

steps.listen(app)
```

First we create a function named step1, we want user name. ask user to send name with `send_message` and set next step for user with `register_next_step`. after all, we use `unregister_steps` to remove steps for user.

end of code, you can see `steps.listen` function. this function listen updates which sends to your client.

> you must use `listen` after all decorators.

Now see `ask` method, this is make code easy for you. see example:
```python
@app.on_message(filters.command("start"))
async def step1(c, msg):
    await steps.ask(
        c, step2, msg.chat.id, "what is your name?",
        user_id=msg.from_user.id
    )

async def step2(c, msg):
    await app.send_message(msg.chat.id, "your name is: %s" % msg.text)
    steps.unregister_steps(msg.from_user.id)

steps.listen(app)
```

If you don't like this step handling, can use `ask_wait` function. see example:
```python
@app.on_message(filters.command("start"))
async def step1(c, msg):
    result = await steps.ask_wait(
        c, step2, msg.chat.id, "what is your name?",
        user_id=msg.from_user.id
    )
    await app.send_message(msg.chat.id, "your name is: %s" % result.text)

steps.listen(app)
```

Let's not forget the `listen_on_the_side` function.
Use this instead `listen` method **if you have a decorator without any filter.**

Example:
```python
@app.on_message() # or @app.on_message(filters.all)
@steps.listen_on_the_side
async def step1(c, msg):
    result = await steps.ask_wait(
        c, step2, msg.chat.id, "what is your name?",
        user_id=msg.from_user.id
    )
    await app.send_message(msg.chat.id, "your name is: %s" % result.text)
```

## New filters

```python
from pyrostep import filters
```

- **ttl_message**: Filter ttl messages ( ttl photo message or ttl video message ).

- **video_sticker**: Filter video sticker messages.

- **entities**: Filter messages include entities.

- **photo_size**: Filter photo messages with width and height.

- **member_of_chats**: Filter users who are members of chats.

## Connection

#### **Function `connection_max_retries`**:

Change connection max retries. (default 3)

**retries message**:
Unable to connect due to network issues: ...

**Return**:
    returns MAX_RETRIES if max_retries is None

#### **Function `invoke_max_retries`**:
Change invoke max retries. (default 5)

**retries message**:
    [...] Waiting for ... seconds before continuing (required by "...")
    
**Return**:
    returns MAX_RETRIES if max_retries is None

#### **Function `session_start_timeout`**:
Change start timeout. (default 1)

**Return**:
    returns START_TIMEOUT if timeout is None. 

#### **Function `session_max_retries`**:
Change session max retries.

retries message:
    Connection failed! Trying again...
    
What is mode? TCP Connection mode.

- TCP Modes:
    - TCPFull
    - TCPAbridged
    - TCPIntermediate
    - TCPAbridgedO
    - TCPIntermediateO

## Other
import shortcuts:
```python
from pyrostep import shortcuts
```

Now see methods:

`split_list` splites lst list:
```python
>>> shortcuts.split_list([1, 2, 3, 4, 5, 6], 2)
# [[1, 2], [3, 4], [5, 6]]
>>> shortcuts.split_list([1, 2, 3], 2)
# [[1, 2], [3]]
```

`keyboard` creates ReplyKeyboardMarkup from your list:
```python
buttons = [
    [
        ["Top Left"], ["Top Right"]
    ],
    [
        ["Bottom | Request Contact", True, "request_contact"]
    ]
]
kb = shortcuts.keyboard(buttons)
```

`inlinekeyboard` creates InlineKeyboardMarkup from your list:
```python
buttons = [
    [
        ["Top Left", "data_1"], ["Top Right", "data_2"]
    ],
    [
        ["Bottom", "Your URL", "url"]
    ]
]
ikb = inlinekeyboard(buttons)
```

`validation_channels` checks user already in channels or not:
```python
user_id = 56392019
channels = [-102792837, -10823823, 'channel_username']

is_joined = await validation_channels(
    app, user_id, channels
)
# ...
async def invite(app, id, channels) -> None:
    print(
        f"User {id} is not member of channels ({channels})"
    )

is_joined = await validation_channels(
    app, user_id, channels,
    invite_func=invite
)
```

# TODO
- Add examples
- Do other tests
