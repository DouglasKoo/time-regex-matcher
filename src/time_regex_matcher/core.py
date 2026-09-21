"""Core extraction and normalization logic.

The implementation deliberately handles a focused set of written time formats
rather than attempting to cover every possible clock expression. It supports:

* 12-hour times with optional ``am``/``pm`` (case-insensitive, with or without
  a separating space) and optional minutes.
* 24-hour times in the 00:00 to 23:59 range.

All extracted times are normalized to 24-hour ``HH:MM`` strings. Minutes are
padded to two digits, and hour-only times are treated as ``HH:00``.

This choice keeps the regular expressions maintainable and predictable for the
unstructured text use case while still handling the most common variants.
"""

from __future__ import annotations

import re
from typing import List, Match, Optional

# A compiled pattern is used for speed because ``extract_times`` is expected to
# be called repeatedly on different text strings.
_TIME_PATTERN = re.compile(
    r"""
    (?<!\d)
    (
        # 12-hour format: 1-12, optional colon, optional two-digit minutes,
        # optional space, am/pm marker.
        (?P<h12>1[0-2]|0?[1-9])
        (?:
            :(?P<m12>[0-5][0-9])
        )?
        \s*
        (?P<ampm>[AaPp]\.?[Mm]\.?)
        |
        # 24-hour format: 00-23:00-59
        (?P<h24>[01]?[0-9]|2[0-3])
        :
        (?P<m24>[0-5][0-9])
    )
    (?!\d)
    """,
    re.VERBOSE,
)


def normalize_time(match: Match[str]) -> str:
    """Normalize a regex match object into a 24-hour ``HH:MM`` string.

    Args:
        match: A match object produced by :data:`_TIME_PATTERN`.

    Returns:
        The normalized time string.
    """
    if match.group("h12") is not None:
        hour = int(match.group("h12"))
        minute = int(match.group("m12") or 0)
        ampm = match.group("ampm").lower()
        if ampm.startswith("p") and hour != 12:
            hour += 12
        elif ampm.startswith("a") and hour == 12:
            hour = 0
        return f"{hour:02d}:{minute:02d}"

    hour = int(match.group("h24"))
    minute = int(match.group("m24"))
    return f"{hour:02d}:{minute:02d}"


def extract_times(text: str) -> List[str]:
    """Extract and normalize times from *text*.

    Times are returned in the order they appear. Overlapping matches are not
    possible because the regex consumes the entire time expression.

    Args:
        text: The unstructured text to search.

    Returns:
        A list of normalized 24-hour time strings.
    """
    return [normalize_time(match) for match in _TIME_PATTERN.finditer(text)]
