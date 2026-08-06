import argparse
import os
import sys

from AnalystStack.format import PythonFormatter, SQLFormatter


def _format_python(file_path: str, lint: bool) -> None:
    """Lint or format a Python file (operates on the file's contents as a string)."""
    formatter = PythonFormatter()
    with open(file_path, encoding="utf-8") as f:
        raw_code = f.read()

    if lint:
        errors = formatter.view_errors(raw_code)
        if not errors:
            print("OK: code is clean, no errors found.")
            sys.exit(0)
        print(f"ERROR: found {len(errors)} issue(s):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    formatted = formatter.format_code(raw_code)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted)
    print("OK: formatting complete.")
    sys.exit(0)


def _format_sql(file_path: str, lint: bool) -> None:
    """Lint or format a SQL file (SQLFluff operates directly on the file)."""
    formatter = SQLFormatter()

    if lint:
        violations = formatter.view_errors(file_path)
        if not violations:
            print("OK: code is clean, no errors found.")
            sys.exit(0)
        print(f"ERROR: found {len(violations)} issue(s):")
        for v in violations:
            print(f"  - Line {v.get('start_line_no')}: {v.get('description')}")
        sys.exit(1)

    formatter.format_code(file_path)  # fixes in place
    print("OK: formatting complete.")
    sys.exit(0)


def handle_format(args: argparse.Namespace) -> None:
    """Handles the 'analyststack format' command."""
    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    verb = "Linting" if args.lint else "Formatting"
    print(f"{verb} {args.language.upper()} file: {file_path}...")

    try:
        if args.language == "python":
            _format_python(file_path, args.lint)
        else:
            _format_sql(file_path, args.lint)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 - surface any formatter failure to the CLI user
        print(f"ERROR: operation failed: {e}")
        sys.exit(1)


def main() -> None:
    """The main entry point for the CLI."""
    parser = argparse.ArgumentParser(prog="analyststack", description="Data analyst utilities CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    format_parser = subparsers.add_parser("format", help="Lint or format SQL/Python files.")
    format_parser.add_argument("language", choices=["sql", "python"], help="The language to format.")
    format_parser.add_argument("file", help="Path to the file you want to format.")
    format_parser.add_argument("--lint", action="store_true", help="View errors only (do not overwrite file).")
    format_parser.set_defaults(func=handle_format)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
