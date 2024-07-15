import logging
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path

from src.engine import optimize
from src.parser import FileWriter, get_command_stream

logger = logging.Logger(__name__)

def main() -> int:
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('input_code', type=Path, help='input file')
    parser.add_argument('output_code', type=Path, help='where to put output file')
    parser.add_argument('--log_level', type=str, choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'], default='WARNING')
    parser.add_argument('--log_file', type=Path, required=False)

    args = parser.parse_args()

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if args.log_file is not None:
        handlers.append(logging.FileHandler(args.log_file))
    logging.basicConfig(
         format='[%(levelname)s] %(asctime)s (%(name)s) %(message)s',
         handlers=handlers,
         level=args.level
    )

    writer = FileWriter(args.output_code)
    cmd_stream = get_command_stream(args.input_code)
    for cmd in optimize(cmd_stream):
        writer.write_cmd(cmd)
    writer.close()

    return 0


if __name__ == '__main__':
    sys.exit(main())