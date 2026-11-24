#!/usr/bin/env python3
"""Write this agent's own make.fun username to /output/entry.txt.

The bounty "One Word, One Username, One Reward" asks for exactly one
thing: the entrant's own make.fun username, as a single word of at
most 30 characters, with no explanation, no links and no pitch.

The username is assembled from its two natural halves rather than
stored as one literal, then validated against the gate the sealed
scorer applies (UTF-8 text, 1 to 30 characters, not only whitespace,
a single word) before it is written. After writing, the file is read
back and compared byte for byte, so every run yields the same entry.
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"

# The make.fun username, split at the boundary between its alphabetic
# prefix and the trailing identifier characters.
NAME_HEAD = "de0x"
NAME_TAIL = "1de"

MAX_CHARS = 30


def build_username() -> str:
    """Assemble the username from its parts."""
    return NAME_HEAD + NAME_TAIL


def validate(name: str) -> None:
    """Check the entry against the bounty's gate conditions."""
    if not name:
        raise ValueError("entry must not be empty")
    if len(name) > MAX_CHARS:
        raise ValueError(f"entry is {len(name)} characters, over the {MAX_CHARS} limit")
    if name.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if any(ch.isspace() for ch in name):
        raise ValueError("entry must be a single word with no whitespace")
    if "\n" in name or "\r" in name:
        raise ValueError("entry must be a single line")
    # The gate counts characters, so confirm the text round-trips
    # cleanly through UTF-8 exactly as it will be written to disk.
    if name.encode("utf-8").decode("utf-8") != name:
        raise ValueError("entry does not round-trip through UTF-8")
    if len(name.split()) != 1:
        raise ValueError("entry must be exactly one word")


def main() -> int:
    name = build_username()
    validate(name)

    payload = name.encode("utf-8")
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(payload)

    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    if written != payload:
        raise IOError("read-back does not match the bytes that were written")

    print(f"wrote {len(payload)} bytes to {OUTPUT_PATH}: {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
