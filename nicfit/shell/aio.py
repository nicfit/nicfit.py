from abc import ABC

from .shell import Shell as _SyncShell


class Shell(_SyncShell, ABC):
    def __init__(self, history_file, event_loop=None):
        super().__init__(history_file)

    async def _execute(self, parsed_cmd: list) -> None:
        raise NotImplementedError()
