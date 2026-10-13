from safety.pii_scrubber import PIIScrubber

s = PIIScrubber()
print(s.scrub("Call me at (555) 123-4567 or 555-123-4567"))
# observed: 'Call me at (555) 123-4567 or [REDACTED]'
print(s.detect("Call me at (555) 123-4567"))
# observed: []
