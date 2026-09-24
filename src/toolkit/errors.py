import sys

def CalcError(cause):
    print(f"Error: {cause}", file=sys.stderr)
    sys.exit(2)