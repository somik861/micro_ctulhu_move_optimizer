import logging
from typing import Generator, Iterable

from src.common import Command, MoveCmd, log_function_call
from itertools import islice

logger = logging.Logger(__name__)


@log_function_call(logger)
def _is_in_conflict(what: list[MoveCmd], with_: list[MoveCmd]) -> bool:
    used_indices: set[int] = set()
    for cmd in what:
        used_indices.add(cmd.source)
        used_indices.add(cmd.dest)

    for cmd in with_:
        if cmd.source in used_indices:
            return True
        if cmd.dest in used_indices:
            return True

    return False


@log_function_call(logger)
def _remove_moves_to_the_same_position(section: list[MoveCmd]) -> list[MoveCmd]:
    """Removes: 'move 1 1'"""
    out: list[MoveCmd] = []
    for move in section:
        if move.source != move.dest:
            out.append(move)

    return out


@log_function_call(logger)
def _join_moves(section: list[MoveCmd]) -> list[MoveCmd]:
    """Modifies: 'move 1 2; move 2 3 -> move 1 3'"""
    out: list[MoveCmd] = []
    to_skip: set[MoveCmd] = set()

    for i, cmd in enumerate(section):
        if cmd in to_skip:
            continue

        replaced = False
        for ni, next_cmd in enumerate(islice(section, i + 1, None), i + 1):
            space = section[i + 1: ni]
            if _is_in_conflict(cmd, space):
                break

            if cmd.domain == next_cmd.domain and cmd.dest == next_cmd.source:
                if _is_in_conflict([cmd, next_cmd], space):
                    break
                to_skip.add(next_cmd)
                out.append(MoveCmd(cmd.domain, cmd.source, next_cmd.dest))
                replaced = True
                break

        if not replaced:
            out.append(cmd)

    return out


@log_function_call(logger)
def _optimize_section(section: list[MoveCmd]) -> list[MoveCmd]:
    section = _join_moves(section)
    # this should be last, as it removes unsupported moves (e.g. move 1 1)
    section = _remove_moves_to_the_same_position(section)
    return section


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
