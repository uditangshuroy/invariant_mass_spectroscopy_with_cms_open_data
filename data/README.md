# Data

This directory contains the CMS Open Data samples used in the analysis, with links to access the dataset and further information. The samples obtained from CMS Open Data are stored in the `raw/` folder in this directory.
Data processed, filtered or generated during analysis are stored in the `interim/` folder and `processed/` folder, in **npy** and **csv** file formats.

## Simplified Data (Part 1)

### $Z \rightarrow \mu^+ \mu^-$: (Notebook 1-3)

**CERN Open Data Description**:
This document contains 10k events where two muon candidates with invariant mass near the mass of Z-boson were observed. The data was selected from the primary dataset DoubleMu 2011. These data were selected for use in education and outreach and contain a subset of the total event information. They are not suitable for a full physics analysis.

Find the dataset and other information here: <https://opendata.cern.ch/record/5208>.

### $Z \rightarrow e^+ e^-$: (Notebook 4)

**CERN Open Data Description**:
This document contains 10k events where two electron candidates with invariant mass near the mass of Z-boson were observed. The data was selected from the primary dataset DoubleElectron 2011. These data were selected for use in education and outreach and contain a subset of the total event information. They are not suitable for a full physics analysis.

Find the dataset and other information here: <https://opendata.cern.ch/record/5207>.

<br>

## Full CMS Data (Part 2)
These datasets are obtained from the parent dataset of the aforementioned datasets.

**CERN Open Data Description**: These data were selected from the primary datasets in order to obtain candidate J/psi and Y events, candidate W and Z boson events, and general di-electron and dimuon spectra. These data were selected for use in education and outreach and contain a subset of the total event information. They are not suitable for a full physics analysis.

Find the dataset and other information here: <https://opendata.cern.ch/record/545>.

### $Z \rightarrow \mu^+ \mu^-$: (Notebook 5-7)

An event was selected if there were two muons in the event with $p_T > 20 \,\text{GeV}$ and $|\eta| < 2.1$ and the invariant mass of the two muons was $> 60 \,\text{GeV}$ and $< 120\,\text{GeV}$.

### $J/\psi \rightarrow \mu^+ \mu^-$: (Notebook 8)

An event was selected if there were two muons in the event, both with $|\eta| < 2.1$, at least one muon was a global muon, the invariant mass of the two muons was $> 2 \,\text{GeV}$ and $< 5\,\text{GeV}$, and they have opposite-sign charge.


*No event-level values were manually modified.*