#!/usr/bin/env python3

"""
Plot neutron and proton occupation bar charts for one state.
This script calls plotting functions and shows all figures at the end.
"""

import os
import sys
import matplotlib.pyplot as plt

# Add project root to Python path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from src import parser
from src import plotting


def main():
  filepath = "data/32Na_2p2h.txt"  # change to your file
  state_name = "0-(1)"            # change to your target state

  root = parser.load_cosmo(filepath)
  state = parser.get_state_by_name(root, state_name)

  if state is None:
    print(f"State {state_name} not found.")
    return

  # Create two figures (no show inside plotting functions)
  plotting.plot_neutron_bar(state)
  plotting.plot_proton_bar(state)

  # Show ALL figures at once
  plt.show()


if __name__ == "__main__":
  main()

