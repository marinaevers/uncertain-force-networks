# Uncertainty-Aware Visual Analysis of Force Networks in 2D Granular Materials

This repository contains the source code for the visual analytics approach presented in the paper:

> M. Evers, A. Naseer, T. G. Murthy, V. Natarajan, T. Bin Masood, D. Weiskopf, and I. Hotz,
> **Uncertainty-Aware Visual Analysis of Force Networks in 2D Granular Materials**,
> *Computer Graphics Forum*, 2026. https://doi.org/10.1111/cgf.70438

The tool supports an uncertainty-aware analysis of force networks in 2D granular materials (photoelastic disk experiments). It combines multiple visualizations that represent different perspectives on uncertainty — as variance, probability, and as an additional variable for thresholding — into a single interactive visual analytics approach.

---

## Citation

If you use this code, please cite our paper:

```bibtex
@article{evers2026uncertainty,
  author  = {Evers, Marina and Naseer, Abrar and Murthy, Tejas G. and Natarajan, Vijay and {Bin Masood}, Talha and Weiskopf, Daniel and Hotz, Ingrid},
  title   = {Uncertainty-Aware Visual Analysis of Force Networks in 2D Granular Materials},
  journal = {Computer Graphics Forum},
  year    = {2026},
  doi     = {10.1111/cgf.70438}
}
```

---

## Overview

Granular materials, such as sand, form complex force networks between particles. Repeated measurements of the same experimental setup can yield different results, making it challenging to identify which structures are intrinsic to the system. This tool enables a joint uncertainty-aware analysis of an ensemble of such measurements.

The visual analytics system consists of three main views:

- **Spatial view** – A glyph-based visualization that encodes the probability of individual particles (disks) belonging to a connected component (force chain) and their spatial variation across realizations.
- **Measure visualizations** – Line charts and heatmaps showing graph-based descriptors (average node degree, average connected component size, number of non-participating nodes) and their variance over changes in packing fraction.
- **Sankey diagram** – Shows the evolution of connected components (force chains) as the packing fraction changes, with interactive threshold controls for force and probability.

---

## Repository Structure

```
.
├── dash/                        # Main Dash application
│   ├── app.py                   # App layout
│   ├── callbacks.py             # Dash callbacks (interactivity)
│   ├── visualizations.py        # Visualization helper functions
│   └── requirements.txt         # Python dependencies for the app
├── sankey_tracking_graph/       # Custom Dash component: Sankey tracking diagram
│   ├── src/                     # JavaScript source
│   ├── sankey_tracking_graph/   # Built Python package
│   └── package.json
└── uncertain_graph_view/        # Custom Dash component: Uncertain graph spatial view
    ├── src/                     # JavaScript source
    ├── uncertain_graph_view/    # Built Python package
    └── package.json
```

---

## Installation

The application relies on two custom Dash components that need to be built and installed before running the main app. It is recommended to use a virtual environment.

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 2. Build and install the custom Dash components

**Sankey tracking graph:**
```bash
cd sankey_tracking_graph
pip install -r requirements.txt
npm install
npm run build
pip install .
cd ..
```

**Uncertain graph view:**
```bash
cd uncertain_graph_view
pip install -r requirements.txt
npm install
npm run build
pip install .
cd ..
```

### 3. Install the remaining dependencies

```bash
cd dash
pip install -r requirements.txt
```

---

## How to Run

From inside the `dash/` folder, start the application with:

```bash
python app.py
```

Then open [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

The app uses basic authentication. Default credentials are defined in `app.py`.

---

## How to Use

The visual analytics workflow follows a top-down navigation strategy: start with an overview of the entire experiment across all packing fractions, then drill down to spatial detail for a selected step.

### Sankey Diagram
Provides an overview of how connected components (force chains) evolve as the packing fraction changes. Click on a column to select a packing fraction, or click on a node to highlight the corresponding disks in the spatial view.

### Measure Visualizations
Line charts show the evolution of graph-based measures (average node degree, average connected component size, number of non-participating nodes) with uncertainty bands. Clicking in the line charts selects the corresponding packing fraction. Heatmaps show how these measures change for varying force threshold $F_t$ and probability threshold $P_t$. Click within the heatmaps to interactively set the thresholds.

### Spatial View
Shows a glyph-based representation of the 2D disk arrangement for the selected packing fraction. Each disk is represented by a radial glyph where:
- Each **slice** corresponds to one measurement realization.
- **Colors** encode the spatial position of the connected component (using a 2D colormap based on the component's barycenter).
- **Light gray slices** indicate that a disk does not participate in a force chain for that realization; the fraction of colored slices encodes the probability of participation.
- **Edges** are drawn with a white-to-black colormap encoding the probability of the edge.
Clicking on a disk highlight the corresponding connected component

Additional options (togglable via the settings panel):
- Switch between **color-based** and **size-based** probability encoding.
- Enable **major/minor force chain** encoding (red = major, blue = minor).
- Reorder glyph slices by color similarity.
- Show spatial deviation of disk positions.
