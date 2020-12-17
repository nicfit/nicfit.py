import os
from abc import ABC

from pygments.token import Token
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.styles.pygments import style_from_pygments_dict


class Shell(ABC):
    PROMPT_STYLE = {
        Token.Pound: "#00aa00",
        Token.Toolbar: '#ffffff bg:#333333',
    }

    def __init__(self, history_file):
        self.key_bindings = KeyBindings()
        self.history = FileHistory(history_file)

        self._completer = None
        self._shell_session = PromptSession(multiline=False,
                                            style=self.prompt_style,
                                            history=self.history,
                                            key_bindings=self.key_bindings,
                                            reserve_space_for_menu=2,
                                            )

        self._started, self._stopped = False, False
        self._stop_status = 0

    def _parse(self, raw_cmd: str) -> list:
        raise NotImplementedError()

    def _execute(self, parsed_cmd: list) -> None:
        raise NotImplementedError()

    @property
    def prompt_style(self):
        return style_from_pygments_dict(self.PROMPT_STYLE)

    def start(self):
        self._started = True

        return self._run()

    def _run(self):
        # Command loop
        while not self._stopped:
            stdout_ctx = self._stdoutContext()

            # Read command
            try:
                with stdout_ctx():
                    cmd_line = await (
                        self._shell_session.prompt_async(self._promptTokens(),
                                                         completer=self._completer,
                                                         bottom_toolbar=self._toolbarTokens())
                    )

                    if not cmd_line:
                        continue
            except EOFError:
                if not os.getenv("IGNOREEOF", False):
                    return
                else:
                    print('Use "exit" to leave the shell.')
                    continue
            except KeyboardInterrupt:
                continue

            # Parse command
            try:
                parsed_cmd = self._parse(cmd_line)
            except ValueError as ex:
                print(str(ex))
                continue

            # Execute command
            await self._execute(parsed_cmd)

        return self._stop_status

    def stop(self, status: int = 0):
        self._stopped = True
        self._stop_status = status or 0

    def _promptTokens(self) -> list:
        return []

    def _toolbarTokens(self, *args, **kwargs) -> list:
        return []

    def _stdoutContext(self):
        return patch_stdout
