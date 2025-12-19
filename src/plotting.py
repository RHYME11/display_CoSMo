# src/plotting.py

"""
Plotting utilities for visualizing neutron and proton occupation numbers.
Each function creates ONE figure and returns it (no plt.show() here).
"""

import matplotlib.pyplot as plt
from typing import Dict


def plot_neutron_bar(state: Dict):
  """
  Create a bar chart for neutron (N) occupation numbers for a single state.

  Parameters
  ----------
  state : dict
      Output of parser.get_state_by_name(...)

  Returns
  -------
  matplotlib.figure.Figure
      The created figure.
  """
  occ_list = state["occupations"]

  orbitals = [o["orbital"] for o in occ_list]
  N_values = [o["N"] for o in occ_list]

  x = range(len(orbitals))

  fig = plt.figure(figsize=(10, 5))
  plt.bar(x, N_values, color="blue", alpha=0.7, label="Neutron (N)")

  plt.xticks(x, orbitals, rotation=45)
  plt.title(f"Neutron Occupation for State {state['name']}")
  plt.ylabel("Neutron Occupation Number")

  # horizontal grid
  plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

  plt.tight_layout()
  return fig


def plot_proton_bar(state: Dict):
  """
  Create a bar chart for proton (Z) occupation numbers for a single state.

  Parameters
  ----------
  state : dict
      Output of parser.get_state_by_name(...)

  Returns
  -------
  matplotlib.figure.Figure
      The created figure.
  """
  occ_list = state["occupations"]

  orbitals = [o["orbital"] for o in occ_list]
  Z_values = [o["Z"] for o in occ_list]

  x = range(len(orbitals))

  fig = plt.figure(figsize=(10, 5))
  plt.bar(x, Z_values, color="red", alpha=0.7, label="Proton (Z)")

  plt.xticks(x, orbitals, rotation=45)
  plt.title(f"Proton Occupation for State {state['name']}")
  plt.ylabel("Proton Occupation Number")

  # horizontal grid
  plt.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.7)

  plt.tight_layout()
  return fig

