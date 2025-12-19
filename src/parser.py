# src/parser.py

"""
Cosmo file parser.

This module provides small helper functions to:
1. Load a .cosmo (XML) file.
2. List all <state> entries.
3. Extract occupation information for a single state.
"""

from typing import Any, Dict, List, Optional
import xml.etree.ElementTree as ET


def load_cosmo(filepath: str) -> ET.Element:
  """
  Load a .cosmo XML file and return the root element.

  Parameters
  ----------
  filepath : str
      Path to the .cosmo (XML) file.

  Returns
  -------
  xml.etree.ElementTree.Element
      Root element of the parsed XML tree.

  Raises
  ------
  FileNotFoundError
      If the file does not exist.
  ET.ParseError
      If the XML is not well-formed.
  """
  tree = ET.parse(filepath)
  root = tree.getroot()
  return root


def _parse_float(value: Optional[str]) -> Optional[float]:
  """
  Safely convert a string to float.

  Returns None if value is None or cannot be converted.
  """
  if value is None:
    return None
  try:
    return float(value)
  except ValueError:
    return None


def list_states(root: ET.Element) -> List[Dict[str, Any]]:
  """
  List all <state> elements in the cosmo file.

  Parameters
  ----------
  root : xml.etree.ElementTree.Element
      Root element returned by load_cosmo().

  Returns
  -------
  List[Dict[str, Any]]
      Each dict contains basic information about one state:
      {
        "name": str,
        "J": str,
        "P": str,
        "T": Optional[float],
        "E": Optional[float],
        "Ex": Optional[float]
      }
  """
  states: List[Dict[str, Any]] = []

  for state_elem in root.findall(".//state"):
    attrib = state_elem.attrib

    state_info: Dict[str, Any] = {
      "name": attrib.get("name"),
      "J": attrib.get("J"),
      "P": attrib.get("P"),
      "T": _parse_float(attrib.get("T")),
      "E": _parse_float(attrib.get("E")),
      "Ex": _parse_float(attrib.get("Ex")),
    }

    states.append(state_info)

  return states


def _parse_state_element(state_elem: ET.Element) -> Dict[str, Any]:
  """
  Internal helper to convert a <state> element
  into a Python dictionary with occupations.
  """
  attrib = state_elem.attrib

  state: Dict[str, Any] = {
    "name": attrib.get("name"),
    "J": attrib.get("J"),
    "P": attrib.get("P"),
    "T": _parse_float(attrib.get("T")),
    "E": _parse_float(attrib.get("E")),
    "Ex": _parse_float(attrib.get("Ex")),
    "occupations": []  # filled below
  }

  occupations: List[Dict[str, Any]] = []

  for child in state_elem:
    if child.tag != "occupation":
      # skip wavefunction, matrix, etc.
      continue

    occ_attr = child.attrib

    occ_info: Dict[str, Any] = {
      "orbital": occ_attr.get("name"),
      "N": _parse_float(occ_attr.get("N")),
      "Z": _parse_float(occ_attr.get("Z")),
    }
    occupations.append(occ_info)

  state["occupations"] = occupations
  return state


def get_state_by_name(root: ET.Element, state_name: str) -> Optional[Dict[str, Any]]:
  """
  Find a <state> by its 'name' attribute and return its data.

  Parameters
  ----------
  root : xml.etree.ElementTree.Element
      Root element returned by load_cosmo().
  state_name : str
      The value of the 'name' attribute, for example "0-(1)".

  Returns
  -------
  dict or None
      A dict with state information and occupations if found,
      otherwise None.

      Example structure:
      {
        "name": "0-(1)",
        "J": "0",
        "P": "-",
        "T": 5.0,
        "E": -258.944,
        "Ex": 0.0,
        "occupations": [
          {"orbital": "0s1", "N": 2.0, "Z": 2.0},
          {"orbital": "0p3", "N": 4.0, "Z": 4.0},
          ...
        ]
      }
  """
  for state_elem in root.findall(".//state"):
    if state_elem.get("name") == state_name:
      return _parse_state_element(state_elem)

  return None

