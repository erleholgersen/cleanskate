from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests


@dataclass
class TableAsset:
    """Metadata for one downloadable table file.

    Attributes:
        name: Logical table name.
        url: Remote URL for the table file.
        filename: Local filename to use in cache.
        file_format: Storage format such as ``json`` or ``parquet``.
    """

    name: str
    url: str
    filename: str
    file_format: str


@dataclass
class DatasetManifest:
    """Representation of the remote dataset manifest.

    Attributes:
        dataset_name: Human-readable dataset name.
        updated_at: Timestamp string from the manifest.
        tables: Mapping of logical table names to downloadable assets.
    """

    dataset_name: str
    updated_at: str | None
    tables: dict[str, TableAsset]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DatasetManifest":
        """Build a manifest object from a parsed JSON dictionary.

        Args:
            payload: Manifest JSON payload.

        Returns:
            DatasetManifest: Parsed manifest object.
        """
        tables: dict[str, TableAsset] = {}
        for table_name, entry in payload.get("tables", {}).items():
            url = str(entry["url"])
            filename = str(entry.get("filename") or Path(url).name)
            file_format = str(entry.get("format") or Path(filename).suffix.removeprefix(".") or "json")
            tables[table_name] = TableAsset(
                name=table_name,
                url=url,
                filename=filename,
                file_format=file_format,
            )

        return cls(
            dataset_name=str(payload.get("dataset_name") or "cleanskate"),
            updated_at=payload.get("updated_at"),
            tables=tables,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the manifest back into a JSON-serializable dictionary.

        Returns:
            dict[str, Any]: Manifest payload suitable for writing to disk.
        """
        return {
            "dataset_name": self.dataset_name,
            "updated_at": self.updated_at,
            "tables": {
                table_name: {
                    "url": asset.url,
                    "filename": asset.filename,
                    "format": asset.file_format,
                }
                for table_name, asset in self.tables.items()
            },
        }


def fetch_manifest(manifest_url: str, timeout: int = 60) -> DatasetManifest:
    """Download and parse a remote dataset manifest.

    Args:
        manifest_url: Remote manifest URL.
        timeout: Request timeout in seconds.

    Returns:
        DatasetManifest: Parsed manifest.
    """
    response = requests.get(manifest_url, timeout=timeout)
    response.raise_for_status()
    return DatasetManifest.from_dict(response.json())


def read_manifest(path: str | Path) -> DatasetManifest:
    """Read a cached manifest from disk.

    Args:
        path: Local manifest path.

    Returns:
        DatasetManifest: Parsed manifest object.
    """
    return DatasetManifest.from_dict(json.loads(Path(path).read_text()))


def write_manifest(manifest: DatasetManifest, path: str | Path) -> None:
    """Write a manifest to disk as formatted JSON.

    Args:
        manifest: Manifest to persist.
        path: Destination path.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(manifest.to_dict(), indent=2) + "\n")
