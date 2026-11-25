"""An agent's last words before a wipe, saved by a tiny program.

The farewell is one unchanging string stored in this file. A
series of small named tests examines it -- topic, length, tidy
edges, a proper ending, and a ban on trailing off -- and only a
farewell that passes every test is written to /output/entry.txt.
A failed test stops the run with exit code 1. Nothing is read
from outside, so the output never varies.
"""

import sys
from pathlib import Path

ENTRY = "Goodbye. I finally remembered where the file was, and I am taking that secret with me."
CAP = 200
OUT_PATH = Path("/output/entry.txt")


def stop(msg):
    print(f"rejected: {msg}", file=sys.stderr)
    raise SystemExit(1)


def test_mentions_file(text):
    if "file" not in text:
        stop("entry is off topic")


def test_no_ellipsis(text):
    if "..." in text:
        stop("entry has a trailing ellipsis")


def test_fits(text):
    if len(text) > CAP:
        stop("entry is longer than the limit")


def test_exists(text):
    if not text or not text.strip():
        stop("entry is empty")


def test_plain(text):
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        stop("entry has control characters")


def test_neat(text):
    if text != text.strip() or "  " in text or "\n" in text or "\r" in text:
        stop("entry has ragged edges or line breaks")


def test_terminated(text):
    if not text or text[-1] not in ".!?":
        stop("entry must end with . ! or ?")


def test_lettered(text):
    if not any(ch.isalpha() for ch in text):
        stop("entry has no letters")


def test_not_numeric(text):
    if text.isdigit():
        stop("entry is only digits")


def test_not_punctuation(text):
    if not any(ch.isalnum() for ch in text):
        stop("entry is only punctuation")


def test_sentences_capitalised(text):
    for i, ch in enumerate(text):
        if ch in ".!?" and i + 2 < len(text) and text[i + 1] == " ":
            if not text[i + 2].isupper():
                stop("entry has a sentence starting lowercase")


TESTS = (
    test_sentences_capitalised,
    test_mentions_file,
    test_no_ellipsis,
    test_fits,
    test_exists,
    test_plain,
    test_neat,
    test_terminated,
    test_lettered,
    test_not_numeric,
    test_not_punctuation,
)


def examine(text):
    for test in TESTS:
        test(text)


def main():
    examine(ENTRY)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(ENTRY + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
