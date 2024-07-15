import logging
from pathlib import Path
from typing import Generator

from src.common import Command, MoveCmd, UnknownCmd, log_function_call

logger = logging.Logger(__name__)

@log_function_call(logger)
def get_command_stream(file: Path) -> Generator[Command, None, None]:
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            parts = line.split('_')
            if parts[1] == 'move':
                yield MoveCmd(parts[0], int(parts[2]), int(parts[3]))
                continue
            yield UnknownCmd(line)


class FileWriter:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._file = open(path, 'w', encoding='utf-8')

    @log_function_call(logger)
    def write_cmd(self, command: Command) -> None:
        if type(command) is UnknownCmd:
            self._file.write(f'{command.text}\n')
        if type(command) is MoveCmd:
            self._file.write(f'{command.domain}_move_{command.source}_{command.dest}')

    @log_function_call(logger)
    def close(self) -> None:
        self._file.close()