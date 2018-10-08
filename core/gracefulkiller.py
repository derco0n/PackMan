# PackMan (https://github.com/derco0n/PackMan):

# gracefullkiller: Fetches SigINT and SIGTERM to raise an event
# in order to exit gracefully (close connections etc. ...)

import signal
from events import Events


class GracefulKiller:
    def __init__(self):
        self.events = Events(('on_kill_now', 'on_initialized'))
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.events.on_initialized()

    def exit_gracefully(self, signum, frame):
        self.events.on_kill_now()

    def debug(self):
        self.events.on_kill_now()