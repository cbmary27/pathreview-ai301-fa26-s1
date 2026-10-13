# Plan

## Diagnosis

### Problem

PIIScrubber does not detect or redact US phone numbers in the parenthesized format (555) 123-4567, even though it detects and redacts the equivalent hyphenated format 555-123-4567.

### Reproduction Evidence

The Unit 2 reproduction demonstrated the problem using PIIScrubber directly:

print(s.scrub('Call me at (555) 123-4567 or 555-123-4567'))

The observed output was:

Call me at (555) 123-4567 or [REDACTED]

The reproduction also showed that:

print(s.detect('Call me at (555) 123-4567'))

returned:

[]

The additional issue tests produced:

21 deselected, 4 xfailed in 1.27s

This demonstrates that (555) 123-4567 is not currently handled by the phone-number detection/redaction logic, while 555-123-4567 is redacted.

The current phone_us regular expression allows an optional ) after the three-digit area code and allows an optional hyphen or period as the separator before the next three digits. It does not allow whitespace at that position. Therefore, the space in (555) 123-4567 prevents the full phone number from matching.

## Scope

### What I Will Change

- safety/pii_scrubber.py - update the phone_us regular expression so that the supported parenthesized US phone format (555) 123-4567 can be detected.
- tests/unit/test_pii_scrubber.py - add or update tests to verify detection and redaction of (555) 123-4567.
- Verify that existing supported formats, including 555-123-4567, continue to work.

### What I Will Not Change

- I will not modify unrelated PII patterns such as email, SSN, international phone numbers, or street addresses.
- I will not change the overall scrub() or detect() implementation unless testing shows that it is necessary for the phone-number fix.
- I will not modify repository setup or application configuration.
- I will not include the temporary claim_draft/test_PII.py reproduction script as part of the implementation.

## Files

Files I expect to touch:

safety/pii_scrubber.py - update the phone_us regular expression.
tests/unit/test_pii_scrubber.py - add or update tests for the affected phone-number format.

The temporary claim_draft/test_PII.py file was created only for the Unit 2 reproduction and is not part of the intended implementation.

## Approach

1. Update the phone_us regular expression in safety/pii_scrubber.py to support the phone formats identified in the reproduction.
2. Update the separator character classes so that a space is accepted in addition to the existing hyphen and period separators. This allows formats such as:
555-123-4567
555 123 4567
555.123.4567
(555) 123-4567
3. Update the country-code portion of the expression so that +1 is matched together rather than allowing the regex to begin at the 1 and leave the + behind. The country-code portion should continue to support the existing 1 format.
4. Update the phone-number boundary handling so that parenthesized numbers such as (555) 123-4567 can be matched as a complete phone number rather than starting the match at 555 and leaving the opening parenthesis behind.
5. Keep the change limited to the phone_us pattern. The scrub() and detect() implementations will not be changed because the reproduction shows that the problem is in the phone-number matching pattern.
6. Add or update unit tests in tests/unit/test_pii_scrubber.py for the affected formats, including (555) 123-4567 and +1-555-123-4567, while retaining coverage for the existing 555-123-4567 format.
7. Run the relevant phone-number tests. The fix will be considered successful when the affected phone numbers are detected and completely replaced by [REDACTED], including the + and parentheses where present.

## Test Plan

### Reproduction Steps

I will re-run the Unit 2 reproduction:

1. Activate the Python virtual environment.
2. Run: PYTHONPATH=. python claim_draft/test_PII.py
3. Verify the output of scrub() for: Call me at (555) 123-4567 or 555-123-4567
4. Verify the result of detect() for: (555) 123-4567

### Expected Result After the Fix

For:

Call me at (555) 123-4567 or 555-123-4567

both phone numbers should be redacted.

The result should therefore contain:

Call me at [REDACTED] or [REDACTED]

The corresponding detect() call should return a phone PII detection for (555) 123-4567 instead of an empty list.

### Pass Condition

The fix passes if:

(555) 123-4567 is detected as phone_us PII.
scrub() replaces (555) 123-4567 with [REDACTED].
555-123-4567 continues to be detected and redacted.
The relevant phone-number tests pass.
The reproduction no longer produces the previously observed unredacted (555) 123-4567 result.

## Risks and Unknowns

Changing the phone_us regular expression could unintentionally affect other supported phone-number formats. Different combinations of country codes, parentheses, spaces, hyphens, and periods should be tested to make sure the updated pattern does not introduce regressions.
The pattern should be tested against both the newly supported (555) 123-4567 format and the existing formats to confirm that the complete phone number is detected and redacted.

## Deviations

