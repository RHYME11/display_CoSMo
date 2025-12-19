#!/usr/bin/env python3

"""
Example: build a simple level scheme from one CoSMo XML file.

This script demonstrates:
1) Loading a CoSMo .cosmo/.xml file.
2) Selecting a subset of states.
3) Choosing a reference energy (E_ref).
4) Computing Ex (keV) from E and E_ref.
5) Plotting a basic level scheme using src/level_scheme.py with display toggles.
"""

import os
import sys
import matplotlib.pyplot as plt

# Add project root to Python path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from src import parser
from src import level_scheme


def build_jp(state_summary: dict) -> str:
  """
  Build a simple Jπ string like '2-' or '0-'.
  """
  J = state_summary.get("J", "")
  P = state_summary.get("P", "")
  return f"{J}{P}"


def main():
  # ---------------------------------------------------------
  # Input
  # ---------------------------------------------------------
  filepath = "data/32Na_2p2h.txt"  # change to your file
  root = parser.load_cosmo(filepath)

  # ---------------------------------------------------------
  # Select states (example selection by name)
  # ---------------------------------------------------------
  all_states = parser.list_states(root)

  # Example: choose a few states by name
  selected_names = ["0-(1)", "3-(1)", "2-(1)", "4-(1)", "5-(1)", "4-(2)"]
  selected_states = [s for s in all_states if s["name"] in selected_names]

  if len(selected_states) == 0:
    print("No states matched selected_names.")
    return

  # ---------------------------------------------------------
  # Choose reference energy E_ref
  # ---------------------------------------------------------
  # Default: use the lowest E in THIS file as the reference
  E_ref = min(s["E"] for s in all_states if s["E"] is not None)

  # Alternative (optional): reference to a specific state name
  # ref_name = "0-(1)"
  # ref_state = next((s for s in all_states if s["name"] == ref_name), None)
  # if ref_state is None or ref_state["E"] is None:
  #   print(f"Reference state {ref_name} not found or has no E.")
  #   return
  # E_ref = ref_state["E"]

  # ---------------------------------------------------------
  # Build levels for plotting
  # ---------------------------------------------------------
  levels = []
  for st in selected_states:
    if st["E"] is None:
      continue

    ex_keV = (st["E"] - E_ref) * 1000.0

    levels.append({
      "energy_keV": ex_keV,
      "state_name": st["name"],
      "jp": build_jp(st)  # only shown if show_jp=True below
    })

  # ---------------------------------------------------------
  # Plot
  # ---------------------------------------------------------
  # Your current preference:
  # - no "keV" after energy (handled in src/level_scheme.py)
  # - do NOT show Jπ (middle info) -> show_jp=False
  # - show energy and (state_name)
  level_scheme.plot_level_scheme(
    levels,
    title="Level scheme (example): selected states",
    show_energy=True,
    show_state_name=True,
    show_jp=False,
    energy_decimals=1,
    level_color="black"
  )

  plt.show()


if __name__ == "__main__":
  main()

