#!/usr/bin/env python3
"""
Generate a gallery figure of all custom colormaps.

Each colormap is displayed as a horizontal bar with its name listed on the
left-hand side, matching the requested layout for quickly browsing palettes.

The resulting figure is saved into the `Plots` directory.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

import colormap_utils as cmap_utils


def _normalize_names(names: Iterable[str]) -> list[str]:
    """Return a list of clean display names."""
    display = []
    for name in names:
        # Keep original ordering and spacing, but make it more legible.
        display.append(name.replace("_", " ").title())
    return display


def build_colormap_gallery(
    colormap_names: Sequence[str],
    output_path: Path,
    samples: int = 512,
) -> Path:
    """
    Build and save the requested gallery figure.

    Parameters
    ----------
    colormap_names : sequence of str
        Names of colormaps to include (case-insensitive).
    output_path : Path
        Where to save the PNG output.
    samples : int
        Number of evenly spaced samples per colormap.
    """
    if not colormap_names:
        raise ValueError("No colormaps specified for gallery.")

    gradient = np.linspace(0.0, 1.0, samples).reshape(1, -1)
    display_names = _normalize_names(colormap_names)

    nrows = len(colormap_names)
    fig_height = 0.55 * nrows + 0.8
    fig, axes = plt.subplots(
        nrows,
        1,
        figsize=(5.0, fig_height),
        constrained_layout=False,
    )

    if nrows == 1:
        axes = [axes]

    plt.subplots_adjust(left=0.28, right=0.96, top=0.98, bottom=0.05, hspace=0.22)

    for ax, cmap_name, label in zip(axes, colormap_names, display_names):
        cmap = cmap_utils.get_colormap(cmap_name)
        ax.imshow(gradient, aspect="auto", cmap=cmap)
        ax.set_axis_off()

        # Add rounded border similar to reference figure.
        border = FancyBboxPatch(
            (0.0, 0.0),
            1.0,
            1.0,
            transform=ax.transAxes,
            boxstyle="round,pad=0.02",
            linewidth=1.2,
            edgecolor="#5fa1ff",
            facecolor="none",
        )
        ax.add_patch(border)

        ax.text(
            -0.08,
            0.5,
            label,
            transform=ax.transAxes,
            ha="right",
            va="center",
            fontsize=10,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_path


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    plots_dir = script_dir / "Plots"
    output_file = plots_dir / "custom_colormaps_gallery.png"

    colormap_names = cmap_utils.list_available_colormaps()
    saved = build_colormap_gallery(colormap_names, output_file)
    print(f"Gallery saved to: {saved}")


if __name__ == "__main__":
    main()
