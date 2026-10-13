I reproduced the phone-number redaction issue described in #53. The current `phone_us` pattern redacts `555-123-4567` but does not redact `(555) 123-4567`.

I plan to update the `phone_us` pattern in `safety/pii_scrubber.py` and update the affected tests in `tests/unit/test_pii_scrubber.py`. I will verify the behavior across the affected phone-number formats and make sure the existing supported formats continue to work.

I have not changed the implementation yet; the changes will be made after confirming the relevant phone-number formats and test expectations.
