#!/usr/bin/env python3
"""Insert or validate canary-token placement in prompt text.

The script implements the project canary rules without embedding any real token.
Pass the raw token via --token; output uses a wrapped <TOKEN> form.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

TRIGGERS = {".", "!", "?", "\n"}


def wrapped_token(token: str) -> str:
    if not token:
        raise ValueError("token must be non-empty")
    if token.startswith("<") and token.endswith(">"):
        return token
    return f"<{token}>"


def is_sentence(segment: str) -> bool:
    candidate = segment.strip()
    return len(candidate) > 3 and len(set(candidate)) > 2


def strip_canaries(text: str, token: str) -> str:
    return text.replace(wrapped_token(token), "")


def insert_canaries(text: str, token: str) -> str:
    marker = wrapped_token(token)
    out: list[str] = []
    segment: list[str] = []
    inserted_first = False
    trigger_count = 0
    sentence_count = 0

    for char in text:
        if char in TRIGGERS:
            trigger_count += 1
            if is_sentence("".join(segment)):
                sentence_count += 1

            out.append(char)

            should_insert = False
            if not inserted_first:
                should_insert = True
                inserted_first = True
            elif sentence_count >= 5 or trigger_count >= 10:
                should_insert = True

            if should_insert:
                out.append(marker)
                trigger_count = 0
                sentence_count = 0

            segment = []
        else:
            out.append(char)
            segment.append(char)

    return "".join(out)


def check_canaries(text: str, token: str) -> tuple[bool, str]:
    raw = strip_canaries(text, token)
    expected = insert_canaries(raw, token)
    if text == expected:
        return True, "canary placement is valid"

    diff = difflib.unified_diff(
        text.splitlines(keepends=True),
        expected.splitlines(keepends=True),
        fromfile="actual",
        tofile="expected",
        n=3,
    )
    return False, "".join(diff)


def read_text(path: str | None) -> str:
    if path is None or path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | None, text: str) -> None:
    if path is None:
        sys.stdout.write(text)
    else:
        Path(path).write_text(text, encoding="utf-8")


def run_self_test() -> None:
    token = "CANARY_TOKEN"
    marker = wrapped_token(token)

    cases = [
        (
            "first trigger insertion",
            "ABCD. Tail",
            f"ABCD.{marker} Tail",
        ),
        (
            "five sentence insertion after reset",
            "ABCD. Alpha! Bravo? Coda. Delta! Echo?",
            f"ABCD.{marker} Alpha! Bravo? Coda. Delta! Echo?{marker}",
        ),
        (
            "ten triggers even when not sentences",
            "A.B.C.D.E.F.G.H.I.J.K.",
            f"A.{marker}B.C.D.E.F.G.H.I.J.K.{marker}",
        ),
        (
            "short low-entropy segments are not sentences",
            "ABCD. aa! aa? aa. aa! aa? Valid.",
            f"ABCD.{marker} aa! aa? aa. aa! aa? Valid.",
        ),
    ]

    for name, source, expected in cases:
        actual = insert_canaries(source, token)
        if actual != expected:
            raise AssertionError(f"{name} failed:\nactual={actual!r}\nexpected={expected!r}")
        valid, details = check_canaries(expected, token)
        if not valid:
            raise AssertionError(f"{name} check failed:\n{details}")

    invalid = "ABCD. Alpha! Bravo? Coda. Delta! Echo?"
    valid, _ = check_canaries(invalid, token)
    if valid:
        raise AssertionError("invalid uninstrumented prompt unexpectedly passed")

    print("self_test=PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    insert = sub.add_parser("insert", help="insert canary tokens into prompt text")
    insert.add_argument("path", nargs="?", help="input path, or stdin when omitted")
    insert.add_argument("--token", required=True, help="raw canary token or already wrapped <TOKEN>")
    insert.add_argument("--output", help="output path; stdout when omitted")

    check = sub.add_parser("check", help="validate canary placement in prompt text")
    check.add_argument("path", nargs="?", help="input path, or stdin when omitted")
    check.add_argument("--token", required=True, help="raw canary token or already wrapped <TOKEN>")

    sub.add_parser("self-test", help="run deterministic built-in tests")

    args = parser.parse_args()

    if args.command == "self-test":
        run_self_test()
        return 0

    text = read_text(args.path)
    if args.command == "insert":
        write_text(args.output, insert_canaries(text, args.token))
        return 0

    if args.command == "check":
        valid, details = check_canaries(text, args.token)
        if valid:
            print(details)
            return 0
        sys.stderr.write(details)
        return 1

    raise AssertionError(f"unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
