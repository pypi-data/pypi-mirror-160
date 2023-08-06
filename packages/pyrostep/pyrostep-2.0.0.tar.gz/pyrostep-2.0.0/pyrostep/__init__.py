__author__ = "aWolver"
__version__ = "2.0.0"

from . import shortcuts
from . import steps, filters, connection

def path_to_client(app) -> bool:
    """
    path_to_client paths steps methods to Client type.

    Methods:
        - `steps.listen` as listen
        - `steps.listen_on_the_side` as listen_on_the_side
        - `steps.register_next_step` as register_next_step
        - `steps.unregister_steps` as unregister_steps
        - `steps.ask` as ask
        - `steps.ask_wait` as ask_wait
        - `steps.clear` as clear

    Example::

        app = Client(...)

        path_to_client(app)

        # ...

        name = await app.ask_wait(12984319, "Whats your name?")

        app.listen() # don't forget it
    """
    app.listen = steps.listen
    app.listen_on_the_side = steps.listen_on_the_side
    app.register_next_step = steps.register_next_step
    app.unregister_steps = steps.unregister_steps
    app.ask = steps.ask
    app.ask_wait = steps.ask_wait
    app.clear = steps.clear
