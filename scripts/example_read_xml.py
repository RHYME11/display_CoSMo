#!/usr/bin/env python3
"""
Example script demonstrating how to use src/parser.py
to read a CoSMo .cosmo (XML) output file.

This script:
1. Loads the XML file.
2. Lists all states with their basic attributes.
3. Retrieves one specific state and prints its occupation table.
"""

import os
import sys

# Add project root to Python path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)



from src import parser


def main():
  # ---------------------------------------------------------
  # Load the XML (.cosmo) file
  # ---------------------------------------------------------
  filepath = "data/32Na_2p2h.txt"   # change path if needed
  root = parser.load_cosmo(filepath)

  print("\n=== Loaded XML File ===")
  print(f"File: {filepath}")

  # ---------------------------------------------------------
  # List all states
  # ---------------------------------------------------------
  print("\n=== All States Found ===")
  states = parser.list_states(root)

  for st in states:
    print(f"{st['name']:>8}   J={st['J']:<3}  P={st['P']}   Ex={st['Ex']} MeV")

  # ---------------------------------------------------------
  # Get one state by name
  # ---------------------------------------------------------
  state_name = "0-(1)"    # choose any state from the list above
  state = parser.get_state_by_name(root, state_name)

  print(f"\n=== Occupation Data for State {state_name} ===")
  if state is None:
    print("State not found!")
    return

  print(f"J={state['J']},  P={state['P']},  Ex={state['Ex']} MeV")
  print("Orbital       N (neutron)      Z (proton)")
  print("------------------------------------------")

  for occ in state["occupations"]:
    orb = occ["orbital"]
    N   = occ["N"]
    Z   = occ["Z"]
    print(f"{orb:10s}   {N:10.4f}      {Z:10.4f}")


if __name__ == "__main__":
  main()

