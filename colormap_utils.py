#!/usr/bin/env python3
"""
Custom colormap utilities.

This module parses the XPM colormap definitions stored in `./colormaps`, builds
`matplotlib.colors.ListedColormap` objects for each file, and exposes helper
functions that make it easy to reuse the palettes across scripts.  In
particular, it offers:

* `get_colormap(name)` / `list_available_colormaps()` to access the palettes.
* `create_normalizer()` and `map_values()` to support autorange or user-defined
  min/max (defaulting to `[0, 1]`) for any colormap.
* `register_with_matplotlib()` to add the colormaps to Matplotlib's registry so
  they can be referenced in pyplot just like the built-in ones.

Typical usage
-------------
>>> from colormap_utils import get_colormap, map_values
>>> cmap = get_colormap("viridis")
>>> rgba = map_values([0.0, 0.5, 1.0], "magma", vmin=0.0, vmax=1.0)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Tuple

import numpy as np
from matplotlib import colormaps
from matplotlib import colors as mpl_colors
from matplotlib.colors import ListedColormap, Normalize

COLORMAP_DIR = Path(__file__).resolve().parent / "colormaps"


def _parse_xpm_file(path: Path) -> ListedColormap:
    """
    Parse an XPM colormap file into a Matplotlib ListedColormap.

    The XPM files in `./colormaps` contain a single row of pixels whose colors
    encode the palette we want to reuse.
    """
    raw_lines = path.read_text(encoding="utf-8").splitlines()
    records: List[str] = []
    for line in raw_lines:
        stripped = line.strip()
        if stripped.startswith('"'):
            # Remove trailing terminators.
            records.append(stripped.strip('",;}'))
    if not records:
        raise ValueError(f"File {path} does not contain valid XPM data.")

    header = records[0]
    try:
        width, height, color_count, chars_per_pixel = map(int, header.split())
    except Exception as exc:
        raise ValueError(f"Invalid XPM header in {path}: {header}") from exc

    color_records = records[1 : 1 + color_count]
    pixel_records = records[1 + color_count : 1 + color_count + height]

    color_table: Dict[str, str | None] = {}
    for entry in color_records:
        symbol = entry[:chars_per_pixel]
        remainder = entry[chars_per_pixel:].strip()
        tokens = remainder.split()
        hex_color: str | None = None
        if "c" in tokens:
            idx = tokens.index("c")
            if idx + 1 < len(tokens):
                value = tokens[idx + 1]
                if value.lower() != "none":
                    hex_color = value
        color_table[symbol] = hex_color

    colors_list: List[Tuple[float, float, float]] = []
    for line in pixel_records:
        if len(line) != width * chars_per_pixel:
            raise ValueError(
                f"Line length mismatch in {path}: expected {width * chars_per_pixel}, got {len(line)}"
            )
        for idx in range(0, len(line), chars_per_pixel):
            symbol = line[idx : idx + chars_per_pixel]
            hex_color = color_table.get(symbol)
            if not hex_color:
                # Skip transparent/background entries.
                continue
            colors_list.append(mpl_colors.to_rgb(hex_color))

    if not colors_list:
        raise ValueError(f"No usable colors extracted from {path}.")

    return ListedColormap(colors_list, name=path.stem)


def _load_all_colormaps(directory: Path) -> Mapping[str, ListedColormap]:
    colormap_files = sorted(directory.glob("*.xpm"))
    if not colormap_files:
        raise FileNotFoundError(f"No XPM files found in {directory}")
    collection = {}
    for file in colormap_files:
        cmap = _parse_xpm_file(file)
        collection[file.stem.lower()] = cmap
    return collection


CUSTOM_COLORMAPS: Mapping[str, ListedColormap] = _load_all_colormaps(COLORMAP_DIR)


def list_available_colormaps() -> Tuple[str, ...]:
    """Return the names of all custom colormaps."""
    return tuple(sorted(CUSTOM_COLORMAPS.keys()))


def get_colormap(name: str) -> ListedColormap:
    """Retrieve a custom colormap by name (case insensitive)."""
    key = name.lower()
    if key not in CUSTOM_COLORMAPS:
        raise KeyError(
            f"Colormap '{name}' not found. Available: {', '.join(list_available_colormaps())}"
        )
    return CUSTOM_COLORMAPS[key]


def create_normalizer(
    vmin: float | None = 0.0,
    vmax: float | None = 1.0,
    data: Iterable[float] | np.ndarray | None = None,
    clip: bool = True,
) -> Normalize:
    """
    Build a Normalize object that maps data values into [0, 1].

    Parameters
    ----------
    vmin, vmax : float or None
        Desired lower/upper bounds. If either is None, the missing bound will
        be inferred from `data` (when provided) or fall back to 0/1.
    data : iterable, optional
        When provided, its min/max are used for autoranging whenever vmin or
        vmax is left unspecified.
    clip : bool
        Whether to clip out-of-range values.
    """
    data_array: np.ndarray | None = None
    if data is not None:
        if isinstance(data, np.ndarray):
            data_array = data.astype(float, copy=False)
        else:
            data_array = np.asarray(list(data), dtype=float)
        if data_array.size == 0:
            raise ValueError("Autorange requested but `data` is empty.")
    if vmin is None:
        if data_array is not None:
            vmin = float(data_array.min())
        else:
            vmin = 0.0
    if vmax is None:
        if data_array is not None:
            vmax = float(data_array.max())
        else:
            vmax = 1.0
    if vmax == vmin:
        raise ValueError("vmin and vmax must differ to build a normalizer.")
    return Normalize(vmin=vmin, vmax=vmax, clip=clip)


def map_values(
    values: Iterable[float] | np.ndarray,
    colormap: str,
    vmin: float | None = None,
    vmax: float | None = None,
    autorange: bool = True,
) -> np.ndarray:
    """
    Convert numeric values into RGBA colors using a custom colormap.

    Parameters
    ----------
    values : iterable
        Data to map.
    colormap : str
        Colormap name (see `list_available_colormaps`).
    vmin, vmax : float or None
        Explicit range. When omitted, `[0, 1]` is used unless `autorange` is
        True, in which case the bounds come from the data.
    autorange : bool
        If True and either vmin or vmax is None, compute that bound from
        `values`.
    """
    arr = np.asarray(values, dtype=float)
    data_for_norm = arr if autorange and (vmin is None or vmax is None) else None
    norm = create_normalizer(vmin=vmin, vmax=vmax, data=data_for_norm)
    cmap = get_colormap(colormap)
    return cmap(norm(arr))


def sample_colormap(
    name: str, samples: int = 256, vmin: float = 0.0, vmax: float = 1.0
) -> np.ndarray:
    """Return evenly sampled RGBA colors from a colormap between vmin and vmax."""
    values = np.linspace(vmin, vmax, samples)
    return map_values(values, name, vmin=vmin, vmax=vmax, autorange=False)


def register_with_matplotlib(prefix: str = "custom_") -> None:
    """
    Register every custom colormap with Matplotlib.

    After invoking this function, the colormaps can be referenced by name such
    as `plt.get_cmap("custom_viridis")`.
    """
    for name, cmap in CUSTOM_COLORMAPS.items():
        colormaps.register(cmap, name=f"{prefix}{name}")


__all__ = [
    "CUSTOM_COLORMAPS",
    "COLORMAP_DIR",
    "create_normalizer",
    "get_colormap",
    "list_available_colormaps",
    "map_values",
    "register_with_matplotlib",
    "sample_colormap",
]
