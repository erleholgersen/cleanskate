# Provenance And Citation

`cleanskate` packages parsed figure skating score data for analysis. The
underlying source material comes from public competition results, standings,
officials pages, and detailed protocol pages published by event organizers and
the International Skating Union.

## What Is Source Data

Source-like fields include values such as skater names, nations, ranks, segment
scores, element codes, base values, GOE values, component scores, judge marks,
and officials panels. These are parsed from public result and protocol pages.

The package normalizes those values into related tables so analysts can work in
pandas without scraping each event site themselves.

## What Is Derived

Some columns are derived during parsing and normalization. Important examples
include:

- `event_label`
- `segment_label`
- `attempt_code`
- `element_family`
- `scored_element`
- `invalid_element`
- `clean_element`
- `fall`
- `fall_inferred`
- `call_quarter`
- `call_underrotated`
- `call_downgraded`
- `call_edge_attention`
- `call_wrong_edge`

Derived fields are intended to make common analysis easier, but they are not a
replacement for checking source protocols when publishing a sensitive claim.

## Recommended Citation

For public analysis, cite both the original competition result sources and the
`cleanskate` package version or repository snapshot used for data access.

Suggested wording:

> Data accessed with `cleanskate`, a Python package for loading public figure
> skating result and protocol data into pandas. Original results and protocols
> were published by competition organizers and the International Skating Union.

When using a dated dataset snapshot, include the snapshot version as well:

```text
cleanskate dataset snapshot: 2026-04-12-segment-label-cleanup
```

## Analysis Caveat

`latest` is convenient for exploration, but it can change as hosted data is
updated. Use a dated snapshot for work you expect to reproduce later.
