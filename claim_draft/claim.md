#working on issue 53

#Link - https://github.com/codepath/pathreview-ai301-fa26-s1/issues/53

1. Project Setup

I followed the environment requirements as stated in SETUP.md. All commands were run on git bash terminal

Operating System - Windows 11

Environment: (All satisfy the minimum version listed in SETUP.md)

Git - 2.55.0.windows.3
Python - 3.13.13
Node.js - 24.14.0
npm - 11.9.0
Docker - 29.8.0 
Docker Compose - v5.5.1

*Node.js, npm, Docker, and Docker Compose are not required for reproducing this specific issue, but are installed for future development.

2. Issue Reproduction

The PIIScrubber functionality can be tested without running the full application setup or make setup, since this issue is isolated to pii_scrubber.py. I created a small reproduction script containing the following code:

from safety.pii_scrubber import PIIScrubber
s = PIIScrubber()
print(s.scrub('Call me at (555) 123-4567 or 555-123-4567'))
# observed: 'Call me at (555) 123-4567 or [REDACTED]'
print(s.detect('Call me at (555) 123-4567'))
# observed: []

Creating, Activating a Python virtual environment and downloading any necessary imports:

python -m venv .venv
source .venv/Scripts/activate
pip install structlog pytest

To run the test:

PYTHONPATH=. python claim_draft/test_PII.py

*Note: I created a temporary reproduction script named test_PII.py under a folder 'claim_draft' in the repository root for this reproduction. This is not an existing repository folder/file.

Result:

Call me at (555) 123-4567 or [REDACTED]
2026-09-26 18:16:16 [info     ] pii_detected                   count=0 types=0
[]
(.venv)

Running all the extra tests listed in the issue:

pytest -q tests/unit/test_pii_scrubber.py -k "test_us_phone_number_redaction or test_us_phone_formats or test_detect_phone_pii or test_phone_at_start_of_text"

Result:

xxxx                                                                                                                                                                   [100%]
21 deselected, 4 xfailed in 1.27s

The output matches the behavior described in the issue:

(555) 123-4567 remains unredacted
555-123-4567 is redacted
detect() returns an empty list for (555) 123-4567

3. Analysis and Proposed Solution

After testing the regex with additional phone-number formats, I found that the current expression does not properly handle all optional characters and separators in the phone number format. In particular, the test input contains a space after the closing parenthesis ), but the current regex only accounts for periods and hyphens as separators. This prevents the parenthesized format from being matched correctly.

Note: I have not modified the implementation yet. I will test additional phone number formats and variations of the regular expression to determine which cases are currently handled incorrectly. I will also refer to Python's regex documentation to better understand the behavior before proposing a specific change.