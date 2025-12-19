#!/usr/bin/env python3

"""
Plot for selected states:
1) Level scheme for selected states (colors match occupation plot).
2) Neutron occupation numbers (grouped bar chart) for these states in one figure:
   - exclude orbitals: 0s1, 0p3, 0p1
   - annotate each bar with its value (vertical labels)
   - legend includes energy with 'keV'

No files are saved. Figures are shown on screen.
"""

import os
import sys
from typing import Dict, List
import matplotlib.pyplot as plt

# Add project root to Python path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from src import parser
from src import level_scheme


def build_jp(state_summary: Dict) -> str:
  """Return Jπ string like '2-' or '1/2-'."""
  J = state_summary.get("J", "")
  P = state_summary.get("P", "")
  return f"{J}{P}"


def get_neutron_occ_map(state_full: Dict) -> Dict[str, float]:
  """Convert occupations list into a dict: orbital -> N."""
  out = {}
  for occ in state_full["occupations"]:
    out[occ["orbital"]] = float(occ["N"])
  return out


def main():
  filepath = "data/32Na_2p2h.txt"  # change to your input file
  selected_names = ["0-(1)", "3-(1)", "2-(1)", "4-(1)", "5-(1)", "4-(2)"]

  # Orbitals to exclude in the occupation plot
  excluded_orbitals = {"0s1", "0p3", "0p1"}

  # ---------------------------------------------------------
  # Load + list states (summaries)
  # ---------------------------------------------------------
  root = parser.load_cosmo(filepath)
  all_states = parser.list_states(root)

  # Lookup by name
  state_map = {s["name"]: s for s in all_states}

  # Keep order exactly as selected_names
  selected_summaries: List[Dict] = []
  for name in selected_names:
    if name not in state_map:
      print(f"State {name} not found in file.")
      return
    if state_map[name].get("E") is None:
      print(f"State {name} has no valid E.")
      return
    selected_summaries.append(state_map[name])

  # Reference energy: lowest E in this file
  E_ref = min(s["E"] for s in all_states if s.get("E") is not None)

  # ---------------------------------------------------------
  # Assign consistent colors per state (Matplotlib default cycle)
  # ---------------------------------------------------------
  color_cycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
  state_colors = {}
  for i, s in enumerate(selected_summaries):
    state_colors[s["name"]] = color_cycle[i % len(color_cycle)]

  # ---------------------------------------------------------
  # 1) Level scheme (colored lines matching the occupation plot)
  # ---------------------------------------------------------
  levels = []
  for s in selected_summaries:
    ex_keV = (s["E"] - E_ref) * 1000.0
    levels.append({
      "energy_keV": ex_keV,
      "state_name": s["name"],
      "jp": build_jp(s),
      "color": state_colors[s["name"]],
    })

  level_scheme.plot_level_scheme(
    levels,
    title="32Na 2p2h",
    show_energy=True,
    show_state_name=True,
    show_jp=True,
    energy_decimals=1,
    level_color="black"  # fallback color if per-level color is not provided
  )

  # ---------------------------------------------------------
  # 2) Neutron occupation (grouped bars, exclude some orbitals, annotate values)
  # ---------------------------------------------------------
  # Load full state info (with occupations)
  full_states: List[Dict] = []
  for s in selected_summaries:
    st_full = parser.get_state_by_name(root, s["name"])
    if st_full is None:
      print(f"State {s['name']} not found when loading full state data.")
      return
    full_states.append(st_full)

  # Orbital order from the first selected state, excluding some orbitals
  orbitals_all = [occ["orbital"] for occ in full_states[0]["occupations"]]
  orbitals = [orb for orb in orbitals_all if orb not in excluded_orbitals]

  if len(orbitals) == 0:
    print("No orbitals left after applying excluded_orbitals.")
    return

  # Build neutron occupation matrix and legend labels
  N_matrix = []
  legend_labels = []
  for s_summary, s_full in zip(selected_summaries, full_states):
    occ_map = get_neutron_occ_map(s_full)
    N_matrix.append([occ_map.get(orb, 0.0) for orb in orbitals])

    ex_keV = (s_summary["E"] - E_ref) * 1000.0
    legend_labels.append(f"{s_summary['name']}  {build_jp(s_summary)}  {ex_keV:.1f} keV")

  # Plot grouped bars
  fig, ax = plt.subplots(figsize=(12, 6))

  x = list(range(len(orbitals)))
  n_states = len(N_matrix)

  total_width = 0.8
  bar_w = total_width / n_states
  start = -total_width / 2 + bar_w / 2

  for i in range(n_states):
    state_name = selected_summaries[i]["name"]
    color = state_colors[state_name]

    xi = [xx + start + i * bar_w for xx in x]
    bars = ax.bar(
      xi,
      N_matrix[i],
      width=bar_w,
      label=legend_labels[i],
      color=color,
      alpha=0.85
    )

    # Vertical value labels
    labels = ax.bar_label(bars, fmt="%f", fontsize=8, padding=2, rotation=90)
    for t in labels:
      t.set_ha("center")
      t.set_va("bottom")

  ax.set_xticks(x)
  ax.set_xticklabels(orbitals, rotation=45)
  ax.set_ylabel("Neutron occupation N")
  ax.set_title("Neutron occupations for 32Na 2p2h")
  ax.legend(fontsize=9)
  ymax = ax.get_ylim()[1]
  ax.set_ylim(0, ymax * 1.25)

  fig.tight_layout()
  plt.show()


if __name__ == "__main__":
  main()

