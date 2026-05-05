# Analysis Notes

These are a few project-specific caveats worth keeping in mind when doing public
analysis.

## `latest` Is a Moving Snapshot

`Dataset(version="latest")` is convenient, but it is not fully reproducible over
time. For analysis you want to revisit later, prefer a dated snapshot version.

## Some Fields Are Derived

Not every boolean in the public dataset is a raw protocol field.

In particular:

- `clean_element`
- `fall`
- `fall_inferred`
- the `call_*` columns

are all derived from parsed protocol output rather than copied directly from a
single source cell.

## Fall Assignment Is Conservative

Older protocols are not always consistent about element-level fall annotations,
so the parser compares element markings with the result-level fall/deduction
information.

The basic logic is:

- if a protocol marks a fall on a specific element, `fall` is `True` and
  `fall_inferred` is `False`
- if the result reports a fall and there is a narrow, high-confidence way to
  assign it to an element, `fall` is `True` and `fall_inferred` is `True`
- if the result reports a fall but the parser cannot confidently assign it to a
  specific element, the ambiguous element-level `fall` values are left missing
- if the result does not report a fall, element-level `fall` values can be
  `False`

That means:

- `fall == True` is useful for element-level fall filters
- `fall_inferred == True` tells you the assignment came from fallback logic
- missing `fall` values are the caution flag for segment-level ambiguity

## Event Coverage Is Broad But Not Exhaustive

The package now covers a large amount of major senior and junior international
competition data from `2018-2019` onward, but there are still some blocked or
special-case events.

This is especially true in parts of the Challenger Series, where some hosts use
nonstandard sites or make detailed protocol data hard to retrieve.

## Judges And Officials

The package includes:

- `officials`
- `segment_officials`

Those tables are useful for panel analysis. The judge details (name/nationality) are provided exactly as in the protocol sheet, and no attempt is made at reconciliating details across events.
