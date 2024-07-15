import logging
from typing import Generator, Iterable

from src.common import Command, MoveCmd, UnknownCmd, log_function_call

logger = logging.Logger(__name__)


@log_function_call(logger)
def _remove_moves_to_the_same_position(section: list[MoveCmd]) -> list[MoveCmd]:
    out : list[MoveCmd] = []
    for move in section:
        if move.source != move.dest:
            out.append(move)

    return out

@log_function_call(logger)
def _optimize_section(section: list[MoveCmd]) -> list[MoveCmd]:
    return _remove_moves_to_the_same_position(section)


@log_function_call(logger)
def optimize(cmd_stream: Iterable[Command]) -> Generator[Command, None, None]:
    @log_function_call(logger)
    def process_section(sect: list[MoveCmd]) -> Generator[MoveCmd, None, None]:
        if len(sect) == 0:
            return
        
        sect = _optimize_section(sect)
        for cmd in sect:
            yield cmd

    section: list[MoveCmd] = []
    for cmd in cmd_stream:
        if type(cmd) is MoveCmd:
            section.append(cmd)
            continue

        yield from process_section(section)
        section = []
        yield cmd

    yield from process_section(section)
