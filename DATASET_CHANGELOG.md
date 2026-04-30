# Dataset Changelog

This file tracks changes to the hosted `cleanskate` dataset snapshots.

It is separate from [CHANGELOG.md](./CHANGELOG.md), which tracks Python package
changes.

## Unreleased

- No unreleased dataset notes yet.

## Entry Template

Use entries in this format for each published snapshot:

```markdown
## 2026-04-29-example

Coverage:

- Added `event family or season` events.
- Filled `specific gap` in the hosted dataset.

Schema and semantics:

- Added or renamed `field_name`.
- Adjusted `derived field` behavior.

Quality and fixes:

- Fixed `specific parsing issue`.
- Improved `host family` scraping or normalization.

Known gaps:

- `event_or_host`: short note on why it is still missing.
```

## 2026-04-29

Published: `2026-04-30T05:08:56Z`

Snapshot summary:

- This is a date-only reissued snapshot intended to be the cleaner public
  baseline identifier for the current hosted dataset.
- Snapshot row counts:
  - `events`: `164`
  - `segments`: `1298`
  - `results`: `21199`
  - `standings`: `10818`
  - `officials`: `1151`
  - `segment_officials`: `12575`
  - `elements`: `182094`
  - `program_components`: `81215`

Coverage:

- Published a stable hosted snapshot covering major international events from
  `2018-2019` onward, including championships, Grand Prix, Junior Grand Prix,
  and much of the Challenger Series.

Schema and semantics:

- Standardized public segment labels such as `Men SP`, `Women FS`, and
  `Ice Dance RD`.
- Exposed officials and segment-level official assignments in the hosted
  dataset.
- Renamed element call fields to the public `call_*` convention and renamed
  `valid_element` to `scored_element`.

Quality and fixes:

- Improved legacy event identity parsing for older federation-hosted results
  pages.
- Tightened event and discipline normalization across older pages and mixed-host
  events.

Known gaps:

- Some Challenger hosts remain blocked or incomplete, especially where the host
  returns `403`, presents a self-signed SSL certificate, or does not expose
  judges-score PDFs.
