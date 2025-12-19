# src/level_scheme.py

"""
Basic level-scheme plotting.

This module provides:
1) A simple level-scheme plotter (single column).
2) A default label formatter with toggle switches.

No file parsing, no state selection logic, no reference-energy logic.
"""

from typing import List, Dict, Optional
import matplotlib.pyplot as plt


def format_level_label(
  energy_keV: float,
  state_name: Optional[str] = None,
  jp: Optional[str] = None,
  show_energy: bool = True,
  show_state_name: bool = True,
  show_jp: bool = False,
  energy_decimals: int = 1
) -> str:
  """
  Format the label text for one level with toggle switches.

  Notes
  -----
  - No "keV" suffix by default (matches your preference).
  - jp is optional and off by default.
  """
  parts: List[str] = []

  if show_energy:
    fmt = f"{{:.{energy_decimals}f}}"
    parts.append(fmt.format(energy_keV))

  if show_jp and jp:
    parts.append(jp)

  if show_state_name and state_name:
    parts.append(f"({state_name})")

  return "  ".join(parts)


def plot_level_scheme(
  levels: List[Dict],
  title: str = "",
  x_center: float = 0.0,
  half_width: float = 0.35,
  label_dx: float = 0.45,
  fontsize: int = 12,
  level_color: str = "black",
  level_linewidth: float = 2.0,
  # label switches (defaults follow your current preference)
  show_energy: bool = True,
  show_state_name: bool = True,
  show_jp: bool = False,
  energy_decimals: int = 1
):
  """
  Plot a simple single-column level scheme.

  Parameters
  ----------
  levels : list of dict
      Each dict must contain:
        - "energy_keV" : float
      Optional keys (used only if corresponding display switches are on):
        - "state_name" : str
        - "jp"         : str   (e.g., "2-")
      You MAY also pass a prebuilt "label" string; if present, it overrides
      the formatter.

  title : str
      Optional figure title.
  level_color : str
      Uniform color for all levels.
  show_energy/show_state_name/show_jp : bool
      Toggle what to display in the label.
  energy_decimals : int
      Decimal places for the energy display.

  Returns
  -------
  fig, ax
  """
  levels_sorted = sorted(levels, key=lambda d: d["energy_keV"])

  fig, ax = plt.subplots(figsize=(6, 8))

  x1 = x_center - half_width
  x2 = x_center + half_width

  for lv in levels_sorted:
    y = float(lv["energy_keV"])

    # If user provided a custom label, use it directly.
    if "label" in lv and lv["label"] is not None:
      label = str(lv["label"])
    else:
      label = format_level_label(
        energy_keV=y,
        state_name=lv.get("state_name"),
        jp=lv.get("jp"),
        show_energy=show_energy,
        show_state_name=show_state_name,
        show_jp=show_jp,
        energy_decimals=energy_decimals
      )

    # Draw level line (uniform style)
    line_color = lv.get("color", level_color)
    ax.plot([x1, x2], [y, y], color=line_color, linewidth=level_linewidth)

    # Add label
    ax.text(x_center + label_dx, y, label, va="center", fontsize=fontsize)

  if title:
    ax.set_title(title)

  ax.set_ylabel("Energy (keV)")
  ax.set_xlabel("")
  ax.set_xticks([])

  # No grid
  ax.grid(False)

  # Remove box: keep ONLY left y-axis spine
  ax.spines["top"].set_visible(False)
  ax.spines["right"].set_visible(False)
  ax.spines["bottom"].set_visible(False)
  ax.spines["left"].set_visible(True)

  ax.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)

  ax.set_xlim(x_center - 1.0, x_center + 2.5)

  fig.tight_layout()
  return fig, ax

