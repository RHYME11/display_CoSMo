# display_CoSMo

Utilities for parsing and visualizing CoSMo shell-model calculation outputs.

This repository is organized with a clear separation between **core reusable code**
and **analysis / example scripts**, following a workflow-oriented design.

---

## Repository Structure

```text
display_CoSMo/
│
├── src/                    # Core, reusable functionality
│   ├── parser.py           # Parse CoSMo .xml/.cosmo files
│   ├── plotting.py         # Occupation-number bar plots (N / Z)
│   ├── level_scheme.py     # Basic level-scheme plotting
│   └── __init__.py
│
├── scripts/                # Example / analysis scripts
│   ├── example_read_xml.py
│   ├── plot_single_state.py
│   └── example_level_scheme.py
│
├── data/                   # Example CoSMo output files
│
└── README.md

```


## Data Structure Overview

This section documents the hierarchical structure of `.xml` files  
generated from CoSMo calculations and parsed by `src/parser.py`.

Only the high-level hierarchy is shown here; details under each branch  
are omitted for clarity.

```text
cosmo (root)
│
├── valencespace
│     ├── core
│     ├── orbital (multiple)
│     └── outercore
│
├── hamiltonian
│     ├── file (multiple)
│     ├── comment
│     └── reference (multiple)
│
└── system
      ├── rejection (multiple)
      ├── ManyBodyStates
      ├── matrix
      └── state (multiple)
            ├── wavefunction
            └── occupation (multiple)
```
