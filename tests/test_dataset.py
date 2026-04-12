from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import requests

from cleanskate import Dataset
from cleanskate.dataset import DEFAULT_ELEMENT_COLUMNS, DEFAULT_RESULT_COLUMNS
from cleanskate.constants import (
    DEFAULT_OFFICIAL_COLUMNS,
    DEFAULT_SEGMENT_OFFICIAL_COLUMNS,
    DEFAULT_STANDING_COLUMNS,
)
from cleanskate.manifest import DatasetManifest, TableAsset, write_manifest


def test_load_events_and_results_filters(local_dataset: Dataset) -> None:
    """Loader filters should narrow rows using readable fields."""
    events = local_dataset.load_events(event_series="Worlds", event_level="Senior")
    assert list(events["event_label"]) == ["Worlds 2026"]

    results = local_dataset.load_results(season="2025-2026", segment_label="Women SP", event_level="Mixed")
    assert list(results["name"]) == ["Kaori SAKAMOTO"]
    assert list(results.columns) == list(DEFAULT_RESULT_COLUMNS)


def test_load_standings_filters_and_default_columns(local_dataset: Dataset) -> None:
    """Standings should load with readable filters and default public columns."""
    standings = local_dataset.load_standings(
        event_series="Worlds",
        event_level="Senior",
        discipline="Men",
        standing_type="Final",
    )
    assert list(standings["name"]) == ["Ilia MALININ"]
    assert list(standings.columns) == list(DEFAULT_STANDING_COLUMNS)



def test_load_officials_filters_and_default_columns(local_dataset: Dataset) -> None:
    """Officials should load with default public columns."""
    officials = local_dataset.load_officials(nation="ISU")

    assert list(officials["name"]) == ["Karen HOWARD", "Zanna KULIK"]
    assert list(officials.columns) == list(DEFAULT_OFFICIAL_COLUMNS)


def test_load_segment_officials_filters_and_default_columns(local_dataset: Dataset) -> None:
    """Segment officials should filter through segment metadata cleanly."""
    panel = local_dataset.load_segment_officials(
        event_series="Worlds",
        event_level="Senior",
        discipline="Men",
        segment_label="Men FS",
    )

    assert list(panel["role"]) == ["Referee", "Judge No.1"]
    assert list(panel.columns) == list(DEFAULT_SEGMENT_OFFICIAL_COLUMNS)

def test_load_elements_filters_and_default_columns(local_dataset: Dataset) -> None:
    """Elements should expose the default public columns and support family filters."""
    jumps = local_dataset.load_elements(event_series="Worlds", event_level="Senior", element_family="Jump")
    assert list(jumps["element_code"]) == ["4Lz", "3A<"]
    assert list(jumps.columns) == list(DEFAULT_ELEMENT_COLUMNS)


def test_load_elements_supports_attempt_and_clean_filters(local_dataset: Dataset) -> None:
    """Elements should support filtering by attempted code and cleanliness."""
    triple_axels = local_dataset.load_elements(attempt_code="3A")
    assert list(triple_axels["element_code"]) == ["3A<"]

    non_clean = local_dataset.load_elements(clean_element=False)
    assert list(non_clean["element_code"]) == ["3A<"]


def test_load_elements_supports_call_flag_filters(local_dataset: Dataset) -> None:
    """Elements should support filtering by derived call booleans."""
    underrotated = local_dataset.load_elements(call_underrotated=True)
    assert list(underrotated["element_code"]) == ["3A<"]

    clean = local_dataset.load_elements(
        element_family="Jump",
        fall=False,
        invalid_element=False,
        call_downgraded=False,
        call_edge_attention=False,
        call_wrong_edge=False,
    )
    assert list(clean["element_code"]) == ["4Lz", "3A<", "2A"]


def test_reuses_in_memory_table_cache(monkeypatch: pytest.MonkeyPatch, local_dataset: Dataset) -> None:
    """Repeated loads should not reread the same table from disk."""
    read_count = 0
    original_read_table = Dataset._read_table

    def counting_read_table(path: Path) -> pd.DataFrame:
        nonlocal read_count
        read_count += 1
        return original_read_table(path)

    monkeypatch.setattr(Dataset, "_read_table", staticmethod(counting_read_table))

    first = local_dataset.load_elements(event_series="Worlds")
    second = local_dataset.load_elements(event_series="Worlds")

    assert len(first) == len(second) == 3
    assert read_count == 2


def test_load_helpers_for_visible_result_rows(local_dataset: Dataset) -> None:
    """Visible result rows should resolve back to their detailed tables."""
    result_row = local_dataset.load_results(event_series="Worlds").iloc[0]

    elements = local_dataset.load_elements_for_result(result_row)
    program_components = local_dataset.load_program_components_for_result(result_row)

    assert list(elements["name"].unique()) == ["Ilia MALININ"]
    assert list(program_components["component_name"]) == ["Composition"]


def test_expand_judge_scores(local_dataset: Dataset) -> None:
    """Judge-score lists should expand into numbered columns."""
    elements = local_dataset.load_elements(event_label="Worlds 2026", columns=["judge_scores"])
    expanded = local_dataset.expand_judge_scores(elements)

    assert list(expanded.columns) == ["judge_1", "judge_2", "judge_3"]
    assert expanded.iloc[0].tolist() == [3, 3, 3]


def test_uses_cached_tables_when_manifest_is_unavailable(local_dataset_dir: Path) -> None:
    """Local cached tables should still load when the manifest URL is unreachable."""
    dataset = Dataset(
        version="latest",
        base_dir=local_dataset_dir,
        manifest_url="https://does-not-resolve.invalid/latest.json",
    )

    events = dataset.load_events(columns=["event_label", "event_series"])
    assert len(events) == 2
    assert list(events.columns) == ["event_label", "event_series"]


def test_refreshes_stale_cached_tables_when_manifest_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    sample_tables: dict[str, list[dict[str, object]]],
) -> None:
    """A newer manifest should trigger a redownload of stale cached tables."""
    stale_dir = tmp_path / "stale"
    stale_dir.mkdir()

    stale_elements = pd.DataFrame(sample_tables["elements"]).drop(columns=["event_series", "element_family"])
    stale_elements.to_json(stale_dir / "elements.json")
    write_manifest(
        DatasetManifest(dataset_name="cleanskate", updated_at="2000-01-01T00:00:00Z", tables={}),
        stale_dir / "manifest.json",
    )

    remote_manifest = DatasetManifest(
        dataset_name="cleanskate",
        updated_at="2026-04-05T23:11:01Z",
        tables={
            "elements": TableAsset(
                name="elements",
                url="https://storage.example/elements.json",
                filename="elements.json",
                file_format="json",
            )
        },
    )
    fresh_elements = pd.DataFrame(sample_tables["elements"])

    monkeypatch.setattr("cleanskate.dataset.fetch_manifest", lambda manifest_url, timeout=60: remote_manifest)

    def fake_download_file(self: Dataset, asset: TableAsset, destination: Path) -> None:
        fresh_elements.to_json(destination)

    monkeypatch.setattr(Dataset, "_download_file", fake_download_file)

    dataset = Dataset(version="latest", base_dir=stale_dir, manifest_url="https://storage.example/latest.json")
    elements = dataset.load_elements(columns=["event_label", "event_series", "element_family", "element_code"])

    assert list(elements.columns) == ["event_label", "event_series", "element_family", "element_code"]
    assert set(elements["element_family"]) == {"Jump", "Spin"}
    assert dataset.local_manifest() is not None
    assert dataset.local_manifest().updated_at == "2026-04-05T23:11:01Z"


def test_manifest_failure_raises_without_local_files(tmp_path: Path) -> None:
    """Missing local data should still surface the underlying network failure."""
    dataset = Dataset(
        version="latest",
        base_dir=tmp_path,
        manifest_url="https://does-not-resolve.invalid/latest.json",
    )

    with pytest.raises(requests.RequestException):
        dataset.load_events()
