# Scoping Review: Analysis of Reported Limitations in Nigerian Maternal and Child Health Research (2014–2024)

## Project Overview

This repository contains the data analysis component of a scoping review that examined methodological and contextual limitations reported in Nigerian Maternal and Child Health (MCH) research between 2014 and 2024.

The study analyzed 228 peer-reviewed publications to identify recurring research challenges and to understand how these limitations affect the overall quality of evidence within Nigeria’s MCH research landscape.

**Research Question:**
What are the most frequently reported methodological and contextual limitations in maternal and child health research conducted in Nigeria between 2014 and 2024?

## Key Findings

The analysis revealed several important patterns:

* Methodological limitations were reported in nearly all studies (80–100%), while contextual challenges were less commonly mentioned (15–30%).
* Single-site studies reported 16% more concerns about generalizability than multi-site studies, showing how study design influences research quality.
* Rural-based studies faced about 45% more contextual challenges than urban ones, indicating location-based research difficulties.
* All studies (100%) acknowledged some form of limitation, showing a strong culture of research transparency.
* Funding source did not influence whether limitations were reported, suggesting consistent ethical standards across both funded and unfunded studies.

## Analysis Approach

The project used a structured and transparent approach that included data preparation, validation, and multi-dimensional analysis.

### Data Processing and Cleaning

* Organized 228 studies into a structured dataset with over 20 variables.
* Developed a consistent coding system for categorizing limitations.
* Applied validation checks to maintain accuracy and consistency.

### Analytical Framework

Eleven analyses were conducted to examine how limitations appeared across different research dimensions:

1. Broad limitation categories – overall prevalence and distribution
2. Specific limitation codes – detailed mapping of common constraints
3. Facility vs. community settings – influence of research environment
4. Regional comparisons – North vs. South Nigeria
5. Temporal trends – changes over time (2014–2024)
6. Contextual limitation patterns – under-reported operational challenges
7. Topic area variations – differences across MCH subfields
8. Funding impact analysis – effect of funding on study rigor
9. Urban–rural disparities – access and contextual issues
10. Study design complexity – single-site vs. multi-site differences
11. Publication venue analysis – influence of journal type

### Technical Implementation

* Implemented in Python using pandas, matplotlib, numpy, and seaborn.
* Automated generation of figures for use in academic manuscripts.
* Designed a reproducible workflow for transparency and reuse.

## Outputs Generated

* Eleven ready-to-publish visualizations (`outputs/figures/`)
* Clean and documented analysis code (`scripts/clean_analysis.py`)
* Summary tables and insights for manuscript development

## Repository Structure

```
scoping-review-mch-nigeria/
├── scripts/
│   └── clean_analysis.py      # Main analysis pipeline
├── outputs/
│   └── figures/               # Manuscript-ready visualizations
└── README.md                  # Project documentation
```

Note: The full dataset used for this analysis is not included in this repository to protect the copyright and intellectual property of the original studies. The analysis is based on 228 peer-reviewed MCH research articles published between 2014 and 2024.

## Technical Details

### Requirements

Before running the analysis, ensure that the following Python libraries are installed:

* pandas ≥ 1.5.0
* matplotlib ≥ 3.5.0
* numpy ≥ 1.21.0
* seaborn ≥ 0.11.0

Install them all at once using:

```bash
pip install -r requirements.txt
```

### Running the Analysis

Run the following command in your terminal to reproduce the analysis:

```bash
python scripts/clean_analysis.py
```

## Dissemination Plans

The findings from this project are being prepared for:

* Journal publication in peer-reviewed public health or research methodology outlets
* Conference presentations to share insights with the global MCH research community
* Stakeholder briefings for Nigerian research institutions, policymakers, and funders

This work aims to contribute to improving research quality, transparency, and capacity building in Nigeria’s maternal and child health research ecosystem.

## Authors

This repository was developed and maintained by Victor Ekoche Ali, Lead Data Analyst on the Scoping Review team.

## Citation

If you use or reference this repository, please cite as:

Ali, V.E. (2025). *Scoping Review: Analysis of Reported Limitations in Nigerian Maternal and Child Health Research (2014–2024).* GitHub Repository. [https://github.com/ekoche1/scoping-review-mch-nigeria](https://github.com/yourusername/scoping-review-mch-nigeria)

## License

This repository is available for academic and research purposes.
Please cite appropriately if the code or analytical framework is used or adapted.

## Summary

This project demonstrates how structured data analysis can help identify recurring research challenges and guide improvements in study design, reporting, and evidence quality. By highlighting common methodological and contextual limitations, it contributes to building stronger and more transparent maternal and child health research in Nigeria.
