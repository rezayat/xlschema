#!/usr/bin/env python3
"""
Remove Emojis from Markdown Files

This script removes all emoji characters from markdown documents while preserving
the structure and formatting of the document.

Usage:
    python remove_emojis.py input.md [output.md]
    python remove_emojis.py --help

Examples:
    # Remove emojis in-place
    python remove_emojis.py README.md

    # Save to a new file
    python remove_emojis.py README.md README_clean.md

    # Process from stdin to stdout
    cat README.md | python remove_emojis.py

Features:
    - Removes all Unicode emoji characters
    - Preserves markdown structure and formatting
    - Handles emoji sequences and skin tone modifiers
    - Cleans up extra whitespace left by removed emojis
    - Supports both file and stdin/stdout processing
"""

import argparse
import re
import sys
import unicodedata
from pathlib import Path
from typing import Optional


class EmojiRemover:
    """Remove emoji characters from text while preserving formatting."""

    def __init__(self):
        # Unicode emoji ranges (comprehensive list)
        self.emoji_patterns = [
            # Emoticons
            r'[\U0001F600-\U0001F64F]',
            # Symbols & Pictographs
            r'[\U0001F300-\U0001F5FF]',
            # Transport & Map Symbols
            r'[\U0001F680-\U0001F6FF]',
            # Supplemental Symbols and Pictographs
            r'[\U0001F900-\U0001F9FF]',
            # Symbols and Pictographs Extended-A
            r'[\U0001FA70-\U0001FAFF]',
            # Miscellaneous Symbols
            r'[\U00002600-\U000026FF]',
            # Dingbats
            r'[\U00002700-\U000027BF]',
            # Enclosed Alphanumeric Supplement
            r'[\U0001F100-\U0001F1FF]',
            # Enclosed Ideographic Supplement
            r'[\U0001F200-\U0001F2FF]',
            # Regional Indicator Symbols (flags)
            r'[\U0001F1E0-\U0001F1FF]',
            # Keycap Sequences
            r'[\U000020E3]',
            # Skin tone modifiers
            r'[\U0001F3FB-\U0001F3FF]',
            # Variation Selectors
            r'[\U0000FE00-\U0000FE0F]',
            # Zero Width Joiner
            r'[\U0000200D]',
            # Additional symbols that might be rendered as emojis
            r'[\U00002049\U0000203C\U00002139\U00002194-\U00002199]',
            r'[\U000021A9-\U000021AA\U0000231A-\U0000231B\U00002328]',
            r'[\U000023CF\U000023E9-\U000023F3\U000023F8-\U000023FA]',
            r'[\U000024C2\U000025AA-\U000025AB\U000025B6\U000025C0]',
            r'[\U000025FB-\U000025FE\U00002934-\U00002935\U00002B05-\U00002B07]',
            r'[\U00002B1B-\U00002B1C\U00002B50\U00002B55\U00003030\U0000303D]',
            r'[\U00003297\U00003299]',
        ]

        # Compile the regex pattern for better performance
        self.emoji_regex = re.compile('|'.join(self.emoji_patterns))

        # Pattern to clean up multiple spaces left by removed emojis
        self.whitespace_cleanup = re.compile(r'\s{2,}')

        # Pattern to remove emojis from heading lines (preserving structure)
        self.heading_emoji_pattern = re.compile(r'^(\s*#{1,6}\s*)([^\n]*?)(\s*)$', re.MULTILINE)

    def remove_emojis(self, text: str) -> str:
        """
        Remove all emoji characters from text.

        Args:
            text: Input text containing emojis

        Returns:
            Text with emojis removed and whitespace cleaned up
        """
        # Remove emoji characters
        text = self.emoji_regex.sub('', text)

        # Clean up multiple spaces left by removed emojis
        text = self.whitespace_cleanup.sub(' ', text)

        # Clean up spaces at the beginning/end of lines
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            # For heading lines, be more careful about spacing
            if line.strip().startswith('#'):
                # Preserve heading structure but clean up emoji spaces
                cleaned_line = ' '.join(line.split())
                cleaned_lines.append(cleaned_line)
            else:
                # For regular lines, clean up but preserve leading/trailing spaces that matter
                cleaned_line = line.rstrip()
                cleaned_lines.append(cleaned_line)

        return '\n'.join(cleaned_lines)

    def is_emoji_character(self, char: str) -> bool:
        """
        Check if a character is an emoji using Unicode categories.

        Args:
            char: Single character to check

        Returns:
            True if character is an emoji
        """
        # Check Unicode category
        category = unicodedata.category(char)

        # Emoji characters often fall into these categories
        emoji_categories = {'So', 'Sm', 'Sk', 'Sc'}  # Symbol categories

        if category in emoji_categories:
            return True

        # Also check against our emoji regex
        return bool(self.emoji_regex.match(char))

    def process_file(self, input_path: Path, output_path: Optional[Path] = None) -> None:
        """
        Process a markdown file to remove emojis.

        Args:
            input_path: Path to input markdown file
            output_path: Path to output file (defaults to input_path if None)
        """
        try:
            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Remove emojis
            cleaned_content = self.remove_emojis(content)

            # Determine output path
            if output_path is None:
                output_path = input_path

            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)

            print(f"✓ Processed {input_path}")
            if output_path != input_path:
                print(f"  → Saved to {output_path}")

        except FileNotFoundError:
            print(f"Error: File '{input_path}' not found", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied accessing '{input_path}'", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error processing '{input_path}': {e}", file=sys.stderr)
            sys.exit(1)

    def process_stdin(self) -> None:
        """Process markdown content from stdin and output to stdout."""
        try:
            content = sys.stdin.read()
            cleaned_content = self.remove_emojis(content)
            sys.stdout.write(cleaned_content)
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            print(f"Error processing stdin: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point for the emoji removal script."""
    parser = argparse.ArgumentParser(
        description='Remove emoji characters from markdown files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s README.md                    # Remove emojis in-place
  %(prog)s README.md clean.md          # Save to new file
  %(prog)s --test "Hello 👋 World!"   # Test emoji removal
  cat file.md | %(prog)s               # Process from stdin
        """
    )

    parser.add_argument(
        'input_file',
        nargs='?',
        help='Input markdown file (use - or omit for stdin)'
    )

    parser.add_argument(
        'output_file',
        nargs='?',
        help='Output file (defaults to input_file for in-place editing)'
    )

    parser.add_argument(
        '--test',
        metavar='TEXT',
        help='Test emoji removal on provided text string'
    )

    parser.add_argument(
        '--list-emojis',
        action='store_true',
        help='List all emojis found in the input (without removing them)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )

    args = parser.parse_args()

    remover = EmojiRemover()

    # Handle test mode
    if args.test:
        original = args.test
        cleaned = remover.remove_emojis(original)
        print(f"Original: {original}")
        print(f"Cleaned:  {cleaned}")
        return

    # Handle stdin/stdout processing
    if not args.input_file or args.input_file == '-':
        if not sys.stdin.isatty():  # Check if there's piped input
            remover.process_stdin()
        else:
            parser.print_help()
            print("\nError: No input provided. Use a filename or pipe input to stdin.", file=sys.stderr)
            sys.exit(1)
        return

    # Handle file processing
    input_path = Path(args.input_file)
    output_path = Path(args.output_file) if args.output_file else None

    if not input_path.exists():
        print(f"Error: File '{input_path}' does not exist", file=sys.stderr)
        sys.exit(1)

    # List emojis mode
    if args.list_emojis:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            emojis = remover.emoji_regex.findall(content)
            if emojis:
                unique_emojis = list(set(emojis))
                print(f"Found {len(emojis)} emoji characters ({len(unique_emojis)} unique):")
                for emoji in unique_emojis:
                    print(f"  {emoji}")
            else:
                print("No emojis found in the file.")
            return
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Dry run mode
    if args.dry_run:
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()

            cleaned_content = remover.remove_emojis(content)

            if content == cleaned_content:
                print(f"No changes would be made to '{input_path}'")
            else:
                print(f"Changes would be made to '{input_path}':")
                # Show a diff-like output
                original_lines = content.split('\n')
                cleaned_lines = cleaned_content.split('\n')

                for i, (orig, clean) in enumerate(zip(original_lines, cleaned_lines), 1):
                    if orig != clean:
                        print(f"  Line {i}:")
                        print(f"    - {orig}")
                        print(f"    + {clean}")
            return
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Normal processing
    remover.process_file(input_path, output_path)


if __name__ == '__main__':
    main()