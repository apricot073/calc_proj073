from __future__ import annotations

import argparse
import sys

from toolkit.calculator import Calc

def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Console utilities: calculator and unit converter",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser(
        "calc",
        help="Evaluate an arithmetic expression",
        description="Supported operators: + - * / (unary +/- allowed)",
    )
    calc_parser.add_argument(
        "expression",
        help='Expression to evaluate',
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="Convert a value between units",
        description="Groups: length (mm, cm, m, km), mass (g, kg), temperature (c, f, k).",
    )
    convert_parser.add_argument("value", type=float, help="Numeric value to convert")
    convert_parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="Source unit",
    )
    convert_parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="Target unit",
    )

    return parser


def main(argv: list[str]):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "calc":
        my_calc = Calc()
        my_calc.tokenization(args.expression)
        my_calc.validation()
        print(my_calc.calculation())
    elif args.command == "convert":
        print(args.value)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))