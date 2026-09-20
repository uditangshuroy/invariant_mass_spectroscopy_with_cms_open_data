# Invariant-Mass Spectroscopy with CMS Open Data
## _Reconstruction and Characterisation of $Z$ and $J/\psi$ Resonances_

<br>

## Overview
This project investigates the invariant-mass reconstruction of multiple decay channels of the $Z$-boson, as well as the $J/\psi$-meson, utilising principles of relativistic four-vectors and kinematics, massless approximations, selection and validation tests, resonance peak-fitting, and final analyses by the means of goodness-of-fit and other statistical tests.

The project is divided into two parts:
- **Part 1: Simplified CMS Data**. This part comprises of four notebooks and uses a simplified version of $Z$-boson decay events; the data comprising of 10,000 events only. This primarily aims to develop an understanding of the structure of the dataset, and perform the necessary initial inspections required for further, more advanced analysis. It initially analyses $Z \rightarrow \mu^+\mu^-$ dimuon events, and the last notebook of this part focuses on $Z \rightarrow e^+e^-$ di-electron events. Furthermore, it ends with comparing the two analysis to demonstrate the robustness of the invariant-mass spectroscopy methods across the two decay channels.
- **Part 2: Full CMS Data**. This part builds on its predecessor and now derives data from a much larger, less filtered dataset, comprising of 100,000 events. A similar, yet modified to requirements, approach is taken in this part of the project. It begins with the similar $Z \rightarrow \mu^+\mu^-$ dimuon events, however, now with a larger dataset, therefore requiring selection and validation criteria to be implemented. The last notebook focuses on $J/\psi \rightarrow \mu^+\mu^-$ dimuon events, and once again compares the two analyses to illustrate the reproducibility and effectiveness of the invariant-mass spectroscopy methods discussed first in Part 1 of the project.

<br> 

## Physics Objectives

### Part 1
- Understand and inspect the initial simplified dataset of dimuon events.
- Explore and analyse the kinematic properties of the individual muons.
- Reconstruct invariant masses from lepton four-vectors for the dimuon events, and then for the di-electron events.
- Investigate the validity of the massless approximation.

### Part 2
- Validate reconstructed kinematic quantities and select $Z \rightarrow \mu^+\mu^-$ events.
- Reconstruct the Z-boson resonance with the larger, now filtered dataset.
- Compare Gaussian, Breit-Wigner and Voigt models with the obtained invariant-mass data.
- Evaluate goodness-of-fit using $\chi^2$, $p$-values, AIC and BIC tests.
- Reconstruct the $J/\psi$ invariant-mass resonance in a similar way.
- Compare the $Z$ and $J/\psi$ dimuon systems.

<br> 

## Repository Structure
The repository structure is presented below for ease of navigation. All folders, files and data sources are labelled clearly for easy identification. Not all individual files, such as saved images and csv data files, are listed here for brevity.

```text
invariant_mass_spectroscopy_with_cms_open_data/
│
├── README.md
├── LICENSE.txt
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── README.md
│   ├── raw/
|   ├── interim/
│   └── processed/
│
├── notebooks/
|   ├── Part I_Simplified Reconstruction/
│   |   ├── 01_dataset_overview.ipynb
│   |   ├── 02_exploratory_data_analysis.ipynb
│   |   ├── 03_Z_to_mumu_reconstruction.ipynb
│   |   ├── 04_lepton_channel_comparison.ipynb
│   ├── Part II_Full Dataset Analysis/
|   |   ├── 05_dataset_validation.ipynb
│   |   ├── 06_event_selection.ipynb
│   |   ├── 07_independent_Z_boson_reconstruction.ipynb
│   └── └── 08_Z_J_psi_dimuon_resonance.ipynb
│
├── src/
│   ├── __init__.py
│   ├── fit_peaks.py
│   ├── fourvectors.py
│   ├── particles.py
│   ├── selection.py
│   ├── utilities.py
│   ├── plotting.py
│   └── validation.py
│
├── figures/
│   ├── jpsi_mumu_mass_spectrum_part_2.png
│   ├── z_mumu_exact_mass_reconstruction_part_1.png
|   └── ...
│
└── reports/
    ├── Roy_Invariant_Mass_Spectroscopy_with_CMS_Open_Data.pdf
    ├── texcodes/
    |   ├── project_report.tex
    |   └── references.bib
    └── figures/
```

<br> 

## Notebook Descriptions
The notebooks mentioned in the `notebooks/` folder above are described in brief below.

| Notebook | Description |
|---|---|
|**Part 1**|**Simplified CMS Data Analysis**|
| 01 | Dataset introduction and initial analysis |
| 02 | Exploratory data analysis |
| 03 | Invariant-mass derivation |
| 04 | Electron-muon comparison |
|||
|**Part 2**|**Full CMS Data Analysis**|
| 05 | Independent kinematic validation |
| 06 | Event selection of the large dataset |
| 07 | $Z$-boson resonance reconstruction and peak fitting |
| 08 | $J/\psi$-meson comparison and project conclusion |

<br>

## Getting Started

This project requires **Python 3.11+** and **JupyterLab (v4.0 or higher)** to run the notebook suite. It is primarily designed to work in a Windows environment, however, with certain compatibility installations, it can also run in Mac/Linux or other platforms.

All required Python libraries and Jupyter components are listed in `requirements.txt`.

### Installation & Setup

1. Clone the repository:
   ```bash
    git clone https://github.com/uditangshuroy/invariant_mass_spectroscopy_with_cms_open_data.git
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Mac/Linux: source .venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch JupyterLab:
   ```bash
   jupyter lab
   ```

<br>

## Usage
The analysis is implemented in the Jupyter notebooks mentioned above. To ensure the proper flow of analysis, run the notebooks in numerical order:
1. 01_dataset_overview.ipynb
2. 02_exploratory_data_analysis.ipynb
3. 03_Z_to_mumu_reconstruction.ipynb <br>
...

The notebooks use generalised and helper functions contained in Python scripts in the `src/` folder.

<br>

## Data
The project uses simplified CMS Open Data and the full CMS Open Data for analysis. See `data/README.md` for information about the datasets and their sources.

<br>

## Results
The analysis successfully reconstructs resonances near the expected
masses of the $Z$-boson and $J/\psi$-meson. The report in `reports/` folder summarises the project in a scientific manner, and the `data/processed/` folder contains all the saved data from the notebooks.

<br>

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star!

1. **Fork** the Project.
2. Create your **Feature Branch** (`git checkout -b feature/new_feature`).
3. **Commit** your Changes (`git commit -m 'Add some new feature'`).
4. **Push** to the Branch (`git push origin feature/new_feature`).
5. Open a **Pull Request**.

<br>

## License & Open Access

This project uses a multi-license structure:

1. **Source Code & Notebooks (`src/`, `notebooks/`):** 
   Licensed under the [GNU General Public License v3.0](https://ftp.gnu.org/gnu/Licenses/gpl-3.0.txt). More information in `license.txt`, in the main directory folder.

2. **Report, Figures & Documentation (`reports/`, `figures/`):** 
   Licensed under the [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). More information in `reports/license.txt`.

3. **Data (`data/`):** 
   Derived from [CMS Open Data](http://opendata.cern.ch/) (CERN). CMS Open Data is released under the [Creative Commons Zero v1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) license, allowing open access and re-use for education and research.

<br>

## Citation

If you use this analysis or code in your research, please cite:

```bibtex
@misc{uditangshuroy2026invmasscms,
  author       = "Roy, Uditangshu",
  title        = "Invariant-Mass Spectroscopy with {CMS} Open Data",
  year         = "2026",
  howpublished = "\url{https://github.com/uditangshuroy/invariant_mass_spectroscopy_with_cms_open_data}",
  note         = "GitHub repository. Archived versions available through Zenodo, doi: \url{https://doi.org/10.5281/zenodo.22843466}"
}
```

<br>

## Contact
**Author**: Uditangshu Roy

For any queries, business or about the project, contact me:<br>
**Email**    : [roy.uditangshu@gmail.com](mailto:roy.uditangshu@gmail.com) <br>
**LinkedIn** : <https://www.linkedin.com/in/uditangshuroy/>

<br>

Archived on Zenodo. DOI: <https://doi.org/10.5281/zenodo.22843466>

*This repository is maintained for archival and educational purposes. Any suggestions on potential edits or changes welcome. Get in touch at the contact above!*


**Invariant-Mass Spectroscopy with CMS Open Data — August, 2026.**

*Analysis conducted August 2026; final report prepared September 2026.*

---
