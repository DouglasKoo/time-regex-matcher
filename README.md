# Time Regex Matcher

Extracts and normalizes times from unstructured text using regular expressions.

```python
from time_regex_matcher import extract_times

extract_times("Meet at 3:30pm and again at 16:00")
# ['15:30', '16:00']
```

## Why this library exists

Free-form text (chat messages, emails, notes) contains times in many written
formats. This library provides a small, dependency-free way to pull those times
out and convert them to a consistent 24-hour ``HH:MM`` representation. The
trade-off is scope: it handles the common 12-hour and 24-hour clock formats but
does not attempt to parse relative times ("in an hour"), time zones, or date
components.

## Supported formats

- 24-hour times: ``HH:MM`` from ``00:00`` to ``23:59``
- 12-hour times: ``H:MM`` or ``HH:MM`` followed by optional space and ``am`` or
  ``pm`` (case-insensitive, with optional periods)
- Hour-only 12-hour times (``3 pm`` becomes ``15:00``)

Midnight and noon are normalized correctly: ``12 am`` becomes ``00:00`` and
``12 pm`` becomes ``12:00``.

## Edge cases

Times embedded in longer digit sequences (such as ``123:456``) are ignored to
avoid false positives. Minutes are required for 24-hour times, so a bare
``14`` is not extracted.

## API

### `extract_times(text: str) -> list[str]`

Returns all normalized times found in *text* in order of appearance.

### `normalize_time(match: re.Match) -> str`

Converts a regex match object from the internal time pattern to a normalized
24-hour string. Primarily useful for callers who want to reuse the pattern.
