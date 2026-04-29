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

Older protocols are not always consistent about element-level fall annotations.
The dataset uses explicit fall annotations when available and only applies
fallback inference in narrow, high-confidence cases.

That means:

- `fall == True` is useful
- `fall == False` should not be interpreted as "absolutely no fall ever" in all
  historical protocols
- missing `fall` values can indicate segment-level ambiguity

## Event Coverage Is Broad But Not Perfect

The package now covers a large amount of major senior and junior international
competition data from `2018-2019` onward, but there are still some blocked or
special-case events.

This is especially true in parts of the Challenger Series, where some hosts use
nonstandard sites or make detailed protocol data hard to retrieve.

## Judges And Officials

The package includes:

- `officials`
- `segment_officials`

Those tables are useful for panel analysis, but cross-event identity resolution
is still intentionally conservative. The same person may occasionally appear
with slightly different display formatting across events.
