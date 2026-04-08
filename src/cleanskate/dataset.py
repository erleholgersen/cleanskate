from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

import pandas as pd
import requests

from cleanskate.cache import default_cache_dir
from cleanskate.constants import (
    DEFAULT_ELEMENT_COLUMNS,
    DEFAULT_MANIFEST_URL,
    DEFAULT_PROGRAM_COMPONENT_COLUMNS,
    DEFAULT_RESULT_COLUMNS,
    DEFAULT_SEGMENT_COLUMNS,
    DEFAULT_STANDING_COLUMNS,
    TABLE_NAMES,
)
from cleanskate.manifest import (
    DatasetManifest,
    TableAsset,
    fetch_manifest,
    read_manifest,
    write_manifest,
)


class Dataset:
    """Load and cache downloadable score tables for pandas workflows."""

    def __init__(
        self,
        version: str = "latest",
        base_dir: str | Path | None = None,
        manifest_url: str = DEFAULT_MANIFEST_URL,
        timeout: int = 60,
    ) -> None:
        """Initialize a dataset handle.

        Args:
            version: Dataset version to use. ``latest`` is the current default.
            base_dir: Local dataset directory. Defaults to the cleanskate cache.
            manifest_url: Remote URL for the dataset manifest.
            timeout: Request timeout in seconds.
        """
        self.version = version
        self.base_dir = Path(base_dir) if base_dir is not None else default_cache_dir() / version
        self.manifest_url = self._resolve_manifest_url(manifest_url, version)
        self.timeout = timeout
        self._manifest: DatasetManifest | None = None
        self._needs_refresh = False
        self._table_cache: dict[str, pd.DataFrame] = {}

    def prefetch(self, force: bool = False) -> Path:
        """Download all dataset files referenced by the current manifest.

        Args:
            force: Whether to redownload files even if they already exist.

        Returns:
            Path: Local base directory containing cached data files.
        """
        manifest = self.refresh_manifest()
        self.base_dir.mkdir(parents=True, exist_ok=True)

        for asset in manifest.tables.values():
            destination = self.base_dir / asset.filename
            if destination.exists() and not force and not self._needs_refresh:
                continue
            self._download_file(asset, destination)

        self._needs_refresh = False
        return self.base_dir

    def download_latest(self, force: bool = False) -> Path:
        """Backward-compatible alias for downloading the current dataset."""
        return self.prefetch(force=force)

    def refresh_manifest(self) -> DatasetManifest:
        """Fetch the latest remote manifest and cache it on the instance.

        Returns:
            DatasetManifest: Parsed dataset manifest.
        """
        local_manifest = self.local_manifest()
        self._manifest = fetch_manifest(self.manifest_url, timeout=self.timeout)
        self._needs_refresh = self._manifest_has_changed(local_manifest, self._manifest)
        if self._needs_refresh:
            self._table_cache.clear()
        write_manifest(self._manifest, self.local_manifest_path())
        return self._manifest

    def manifest(self) -> DatasetManifest:
        """Return the cached manifest, fetching it if needed.

        Returns:
            DatasetManifest: Current dataset manifest.
        """
        if self._manifest is None:
            try:
                return self.refresh_manifest()
            except requests.RequestException:
                local_manifest = self.local_manifest()
                if local_manifest is None:
                    raise
                self._manifest = local_manifest
                self._needs_refresh = False
                return local_manifest
        return self._manifest

    def local_manifest_path(self) -> Path:
        """Return the cache path for the local manifest file.

        Returns:
            Path: Local manifest JSON path inside the dataset cache.
        """
        return self.base_dir / "manifest.json"

    def local_manifest(self) -> DatasetManifest | None:
        """Read the locally cached manifest when present.

        Returns:
            DatasetManifest | None: Cached manifest, or ``None`` if missing.
        """
        path = self.local_manifest_path()
        if not path.exists():
            return None
        return read_manifest(path)

    def available_tables(self) -> list[str]:
        """List logical table names currently available locally.

        Returns:
            list[str]: Table names whose files can be found in ``base_dir``.
        """
        return [table_name for table_name in TABLE_NAMES if self.table_path(table_name) is not None]

    def table_path(self, table_name: str) -> Path | None:
        """Return the local file path for a table if present.

        Args:
            table_name: Logical table name.

        Returns:
            Path | None: Local path when the table exists, otherwise ``None``.
        """
        if table_name not in TABLE_NAMES:
            raise ValueError(f"Unsupported table name: {table_name}")

        candidate_suffixes = (".parquet", ".json")
        for suffix in candidate_suffixes:
            path = self.base_dir / f"{table_name}{suffix}"
            if path.exists():
                return path

        if self._manifest is not None and table_name in self._manifest.tables:
            manifest_path = self.base_dir / self._manifest.tables[table_name].filename
            if manifest_path.exists():
                return manifest_path

        return None

    def load_table(
        self,
        table_name: str,
        filters: Mapping[str, Any] | None = None,
        columns: Sequence[str] | None = None,
    ) -> pd.DataFrame:
        """Load one table as a pandas data frame.

        Args:
            table_name: Logical table name.
            filters: Optional equality filters by column.
            columns: Optional subset of columns to keep.

        Returns:
            pd.DataFrame: Loaded and filtered table.
        """
        self._ensure_table_available(table_name)
        path = self.table_path(table_name)
        if path is None:
            raise FileNotFoundError(
                f"Table '{table_name}' is not available locally in {self.base_dir}. "
                "The package attempted to fetch it automatically and could not find it."
            )

        frame = self._load_cached_table(table_name, path).copy()
        frame = self.apply_filters(frame, filters)

        if columns is not None:
            missing = [column for column in columns if column not in frame.columns]
            if missing:
                raise KeyError(f"Columns not found in {table_name}: {missing}")
            frame = frame.loc[:, list(columns)]

        return frame

    def load_events(
        self,
        event_id: str | Sequence[str] | None = None,
        event_series: str | Sequence[str] | None = None,
        event_level: str | Sequence[str] | None = None,
        season: str | Sequence[str] | None = None,
        event_label: str | Sequence[str] | None = None,
        columns: Sequence[str] | None = None,
    ) -> pd.DataFrame:
        """Load rows from the ``events`` table."""
        return self.load_table(
            "events",
            filters={
                "event_id": event_id,
                "event_series": event_series,
                "event_level": event_level,
                "season": season,
                "event_label": event_label,
            },
            columns=columns,
        )

    def load_segments(
        self,
        event_id: str | Sequence[str] | None = None,
        event_series: str | Sequence[str] | None = None,
        event_level: str | Sequence[str] | None = None,
        season: str | Sequence[str] | None = None,
        event_label: str | Sequence[str] | None = None,
        segment_id: str | Sequence[str] | None = None,
        discipline: str | Sequence[str] | None = None,
        segment_label: str | Sequence[str] | None = None,
        is_team_event: bool | None = None,
        columns: Sequence[str] | None = None,
    ) -> pd.DataFrame:
        """Load rows from the ``segments`` table."""
        frame = self.load_table(
            "segments",
            filters={
                "event_id": event_id,
                "event_series": event_series,
                "event_level": event_level,
                "season": season,
                "event_label": event_label,
                "segment_id": segment_id,
                "discipline": discipline,
                "segment_label": segment_label,
                "is_team_event": is_team_event,
            },
        )
        if columns is None:
            frame = frame.loc[:, list(DEFAULT_SEGMENT_COLUMNS)]
        else:
            missing = [column for column in columns if column not in frame.columns]
            if missing:
                raise KeyError(f"Columns not found in segments: {missing}")
            frame = frame.loc[:, list(columns)]
        return frame.reset_index(drop=True)

    def load_results(
        self,
        event_id: str | Sequence[str] | None = None,
        event_series: str | Sequence[str] | None = None,
        event_level: str | Sequence[str] | None = None,
        season: str | Sequence[str] | None = None,
        event_label: str | Sequence[str] | None = None,
        segment_id: str | Sequence[str] | None = None,
        segment_label: str | Sequence[str] | None = None,
        discipline: str | Sequence[str] | None = None,
        result_id: str | Sequence[str] | None = None,
        columns: Sequence[str] | None = None,
        include_ids: bool = False,
    ) -> pd.DataFrame:
        """Load rows from the ``results`` table."""
        frame = self.load_table(
            "results",
            filters={
                "segment_id": segment_id,
                "result_id": result_id,
                "event_series": event_series,
                "event_level": event_level,
                "season": season,
                "event_label": event_label,
                "segment_label": segment_label,
            },
        )
        if event_id is not None or discipline is not None:
            segment_ids = self.load_segments(
                event_id=event_id,
                discipline=discipline,
                columns=["segment_id"],
            )["segment_id"]
            frame = frame[frame["segment_id"].isin(segment_ids)]
        if columns is None and not include_ids:
            frame = frame.loc[:, list(DEFAULT_RESULT_COLUMNS)]
        elif columns is not None:
            missing = [column for column in columns if column not in frame.columns]
            if missing:
                raise KeyError(f"Columns not found in results: {missing}")
            frame = frame.loc[:, list(columns)]
        return frame.reset_index(drop=True)

    def load_elements(
        self,
        event_id: str | Sequence[str] | None = None,
        event_series: str | Sequence[str] | None = None,
        event_level: str | Sequence[str] | None = None,
        season: str | Sequence[str] | None = None,
        event_label: str | Sequence[str] | None = None,
        segment_id: str | Sequence[str] | None = None,
        segment_label: str | Sequence[str] | None = None,
        discipline: str | Sequence[str] | None = None,
        element_family: str | Sequence[str] | None = None,
        attempt_code: str | Sequence[str] | None = None,
        clean_element: bool | None = None,
        result_id: str | Sequence[str] | None = None,
        columns: Sequence[str] | None = None,
        include_ids: bool = False,
    ) -> pd.DataFrame:
        """Load rows from the ``elements`` table."""
        frame = self.load_table(
            "elements",
            filters={
                "result_id": result_id,
                "element_family": element_family,
                "attempt_code": attempt_code,
                "clean_element": clean_element,
            },
        )
        if (
            event_id is not None
            or event_series is not None
            or event_level is not None
            or season is not None
            or event_label is not None
            or segment_id is not None
            or segment_label is not None
            or discipline is not None
        ):
            results = self.load_results(
                event_id=event_id,
                event_series=event_series,
                event_level=event_level,
                season=season,
                event_label=event_label,
                segment_id=segment_id,
                segment_label=segment_label,
                discipline=discipline,
                columns=["result_id"],
            )
            frame = frame[frame["result_id"].isin(results["result_id"])]
        if columns is None and not include_ids:
            frame = frame.loc[:, list(DEFAULT_ELEMENT_COLUMNS)]
        elif columns is not None:
            missing = [column for column in columns if column not in frame.columns]
            if missing:
                raise KeyError(f"Columns not found in elements: {missing}")
            frame = frame.loc[:, list(columns)]
        return frame.reset_index(drop=True)

    def load_standings(
        self,
        event_id: str | Sequence[str] | None = None,
        event_series: str | Sequence[str] | None = None,
        event_level: str | Sequence[str] | None = None,
        season: str | Sequence[str] | None = None,
        event_label: str | Sequence[str] | None = None,
        discipline: str | Sequence[str] | None = None,
        standing_type: str | Sequence[str] | None = None,
        columns: Sequence[str] | None = None,
        include_ids: bool = False,
    ) -> pd.DataFrame:
        """Load rows from the ``standings`` table."""
        frame = self.load_table(
            "standings",
            filters={
                "event_id": event_id,
                "event_series": event_series,
                "event_level": event_level,
                "season": season,
                "event_label": event_label,
                "discipline": discipline,
                "standing_type": standing_type,
            },
        )
        if columns is None and not include_ids:
            frame = frame.loc[:, list(DEFAULT_STANDING_COLUMNS)]
        elif columns is not None:
            missing = [column for column in columns if column not in frame.columns]
            if missing:
                raise KeyError(f"Columns not found in standings: {missing}")
            frame = frame.loc[:, list(columns)]
        return frame.reset_index(drop=True)

    def load_program_components(
        self,
        event_id: str | Sequence[str] | None = None,
        event_series: str | Sequence[str] | None = None,
        event_level: str | Sequence[str] | None = None,
        season: str | Sequence[str] | None = None,
        event_label: str | Sequence[str] | None = None,
        segment_id: str | Sequence[str] | None = None,
        segment_label: str | Sequence[str] | None = None,
        discipline: str | Sequence[str] | None = None,
        result_id: str | Sequence[str] | None = None,
        columns: Sequence[str] | None = None,
        include_ids: bool = False,
    ) -> pd.DataFrame:
        """Load rows from the ``program_components`` table."""
        frame = self.load_table("program_components", filters={"result_id": result_id})
        if (
            event_id is not None
            or event_series is not None
            or event_level is not None
            or season is not None
            or event_label is not None
            or segment_id is not None
            or segment_label is not None
            or discipline is not None
        ):
            results = self.load_results(
                event_id=event_id,
                event_series=event_series,
                event_level=event_level,
                season=season,
                event_label=event_label,
                segment_id=segment_id,
                segment_label=segment_label,
                discipline=discipline,
                columns=["result_id"],
            )
            frame = frame[frame["result_id"].isin(results["result_id"])]
        if columns is None and not include_ids:
            frame = frame.loc[:, list(DEFAULT_PROGRAM_COMPONENT_COLUMNS)]
        elif columns is not None:
            missing = [column for column in columns if column not in frame.columns]
            if missing:
                raise KeyError(f"Columns not found in program_components: {missing}")
            frame = frame.loc[:, list(columns)]
        return frame.reset_index(drop=True)

    def load_elements_for_result(self, result_row: pd.Series, include_ids: bool = False) -> pd.DataFrame:
        """Load elements for a visible results row."""
        result_id = self.resolve_result_id(result_row)
        return self.load_elements(result_id=result_id, include_ids=include_ids)

    def load_program_components_for_result(
        self,
        result_row: pd.Series,
        include_ids: bool = False,
    ) -> pd.DataFrame:
        """Load program components for a visible results row."""
        result_id = self.resolve_result_id(result_row)
        return self.load_program_components(result_id=result_id, include_ids=include_ids)

    def resolve_result_id(self, result_row: pd.Series) -> str:
        """Resolve a stable result ID from a visible results row."""
        if "result_id" in result_row.index:
            return str(result_row["result_id"])

        required_columns = ["event_label", "segment_label", "name", "noc", "starting_number"]
        missing = [column for column in required_columns if column not in result_row.index]
        if missing:
            raise KeyError(f"Result row is missing fields required for lookup: {missing}")

        results = self.load_table("results")
        matched = results[
            (results["event_label"] == result_row["event_label"])
            & (results["segment_label"] == result_row["segment_label"])
            & (results["name"] == result_row["name"])
            & (results["noc"] == result_row["noc"])
            & (results["starting_number"] == result_row["starting_number"])
        ]
        if len(matched) != 1:
            raise ValueError("Visible result row did not resolve to exactly one underlying result_id")
        return str(matched.iloc[0]["result_id"])

    @staticmethod
    def expand_judge_scores(
        frame: pd.DataFrame,
        column: str = "judge_scores",
        prefix: str = "judge_",
    ) -> pd.DataFrame:
        """Expand list-valued judge scores into separate columns."""
        if column not in frame.columns:
            raise KeyError(f"Column not found: {column}")
        expanded = pd.DataFrame(frame[column].tolist(), index=frame.index).add_prefix(prefix)
        expanded.columns = [f"{prefix}{index + 1}" for index in range(len(expanded.columns))]
        return pd.concat([frame.drop(columns=[column]), expanded], axis=1)

    @staticmethod
    def apply_filters(
        frame: pd.DataFrame,
        filters: Mapping[str, Any] | None = None,
    ) -> pd.DataFrame:
        """Apply simple equality filters to a data frame.

        Scalar filter values use exact equality. Iterable filter values such as
        lists or tuples use "one of these values" semantics via ``isin``.
        """
        if not filters:
            return frame
        filtered = frame
        for column, value in filters.items():
            if value is None or column not in filtered.columns:
                continue
            if Dataset.is_multi_value(value):
                filtered = filtered[filtered[column].isin(list(value))]
            else:
                filtered = filtered[filtered[column] == value]
        return filtered.reset_index(drop=True)

    @staticmethod
    def is_multi_value(value: Any) -> bool:
        """Return whether a filter value should be treated as many values."""
        return isinstance(value, Iterable) and not isinstance(value, (str, bytes, dict))

    @staticmethod
    def _read_table(path: Path) -> pd.DataFrame:
        """Read a local table file into pandas based on its suffix."""
        if path.suffix == ".parquet":
            return pd.read_parquet(path)
        if path.suffix == ".json":
            return pd.read_json(path)
        raise ValueError(f"Unsupported table format: {path.suffix}")

    def _download_file(self, asset: TableAsset, destination: Path) -> None:
        """Download one table asset into the local cache.

        Args:
            asset: Manifest entry describing the downloadable table.
            destination: Local file path to write.
        """
        destination.parent.mkdir(parents=True, exist_ok=True)
        response = requests.get(asset.url, timeout=self.timeout)
        response.raise_for_status()
        destination.write_bytes(response.content)

    def _ensure_table_available(self, table_name: str) -> None:
        """Ensure a table file exists locally, downloading it on demand.

        Args:
            table_name: Logical table name.
        """
        try:
            manifest = self.refresh_manifest() if self._manifest is None else self.manifest()
        except requests.RequestException:
            if self.table_path(table_name) is not None:
                return
            raise
        if table_name not in manifest.tables:
            return

        asset = manifest.tables[table_name]
        destination = self.base_dir / asset.filename
        if destination.exists() and not self._needs_refresh:
            return

        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._download_file(asset, destination)
        self._table_cache.pop(table_name, None)

    def _load_cached_table(self, table_name: str, path: Path) -> pd.DataFrame:
        """Load one table, reusing an in-memory copy within this dataset handle."""
        cached = self._table_cache.get(table_name)
        if cached is not None:
            return cached

        frame = self._read_table(path)
        self._table_cache[table_name] = frame
        return frame

    @staticmethod
    def _resolve_manifest_url(manifest_url: str, version: str) -> str:
        """Resolve the manifest URL for a requested version.

        Args:
            manifest_url: Base manifest URL or URL template.
            version: Dataset version identifier.

        Returns:
            str: Final manifest URL.
        """
        if "{version}" in manifest_url:
            return manifest_url.format(version=version)
        if version == "latest":
            return manifest_url
        prefix, suffix = manifest_url.rsplit("/", maxsplit=1)
        return f"{prefix}/{version}.json" if suffix == "latest.json" else manifest_url

    @staticmethod
    def _manifest_has_changed(
        previous_manifest: DatasetManifest | None,
        current_manifest: DatasetManifest,
    ) -> bool:
        """Return whether the remote manifest differs from the cached one.

        Args:
            previous_manifest: Cached local manifest when available.
            current_manifest: Newly fetched remote manifest.

        Returns:
            bool: ``True`` when cached table files should be refreshed.
        """
        if previous_manifest is None:
            return True
        if previous_manifest.updated_at != current_manifest.updated_at:
            return True
        return previous_manifest.to_dict() != current_manifest.to_dict()
