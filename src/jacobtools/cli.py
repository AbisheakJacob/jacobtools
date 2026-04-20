import argparse
import os
import sys

# Import the facade we built earlier
from JacobTools.format import format_code


def handle_format(args):
    """Handles the 'jacobtools format' command."""
    file_path = args.file

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    # Read the target file
    with open(file_path, "r", encoding="utf-8") as f:
        raw_code = f.read()

    # Determine which formatter to use
    formatter = format_code.sql if args.language == "sql" else format_code.python

    if args.lint:
        # View Errors Only
        print(f"Linting {args.language.upper()} file: {file_path}...\n")
        errors = formatter.view_errors(raw_code)

        if not errors:
            print("✅ Code is clean! No errors found.")
            sys.exit(0)
        else:
            print(f"❌ Found {len(errors)} issues:")
            for err in errors:
                # Handle SQLFluff dicts vs Python string errors
                if isinstance(err, dict):
                    print(f"  - Line {err.get('start_line_no')}: {err.get('description')}")
                else:
                    print(f"  - {err}")
            sys.exit(1)  # Exit code 1 fails the CI/CD pipeline if errors exist
    else:
        # Format and Overwrite
        print(f"Formatting {args.language.upper()} file: {file_path}...")
        try:
            formatted_code = formatter.format_code(raw_code)

            # Write the formatted code back to the file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(formatted_code)

            print("✅ Formatting complete!")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Formatting failed: {e}")
            sys.exit(1)


def main():
    """The main entry point for the CLI."""
    parser = argparse.ArgumentParser(prog="jacobtools", description="Enterprise CLI for Data Engineering utilities.")

    # Create sub-commands (e.g., 'format', and later you could add 'query')
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Setup the 'format' sub-command ---
    format_parser = subparsers.add_parser("format", help="Lint or format SQL/Python files.")

    # Arguments for 'format'
    format_parser.add_argument("language", choices=["sql", "python"], help="The language to format.")
    format_parser.add_argument("file", help="Path to the file you want to format.")
    format_parser.add_argument("--lint", action="store_true", help="View errors only (do not overwrite file).")

    # Map the command to the function
    format_parser.set_defaults(func=handle_format)

    # Parse arguments and trigger the appropriate function
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
