# Scoping Review: Analysis of Reported Limitations in Nigerian Maternal and Child Health Research (2014–2024)

## Project Overview

This repository contains the data analysis component of a scoping review that examined methodological and contextual limitations reported in Nigerian Maternal and Child Health (MCH) research between 2014 and 2024.

The study analyzed 228 peer-reviewed publications to identify recurring research challenges and to understand how these limitations affect the overall quality of evidence within Nigeria's MCH research landscape.

**Research Question:** What are the most frequently reported methodological and contextual limitations in maternal and child health research conducted in Nigeria between 2014 and 2024?

## Key Findings

The analysis revealed several important patterns:

* Methodological limitations were reported in nearly all studies (80–100%), while contextual challenges were less commonly mentioned (15–30%).
* Single-site studies reported 28% more generalizability concerns than multi-site studies (72.9% vs 56.9%), showing how study design influences research quality.
* Rural-based studies faced about 45% more contextual challenges than urban ones, indicating location-based research difficulties.
* All studies (100%) acknowledged some form of limitation, showing a strong culture of research transparency.
* Funding source did not influence whether limitations were reported, suggesting consistent ethical standards across both funded and unfunded studies.
* The top 5 most frequently reported limitations were generalizability (55.3%), single-site setting (32.0%), sampling method bias (25.9%), other design issues (24.1%), and small sample size (22.8%).
* Important limitation clusters were identified, with single-site settings frequently co-occurring with sampling method bias (10.5% of studies) and small sample sizes (8.8% of studies).

## Study Characteristics

### Dataset Overview
* **Total Studies:** 228 peer-reviewed publications
* **Time Period:** 2014–2024
* **Screening Process:** 2,388 references screened → 539 reports assessed → 228 studies included

### Research Design Distribution
* Cross-sectional: 78 studies (34.2%)
* Qualitative: 64 studies (28.1%) 
* Secondary data analysis: 29 studies (12.7%)
* Mixed-methods: 27 studies (11.8%)
* Cohort: 12 studies (5.3%)
* Other designs: 18 studies (7.9%)

### Geographic Coverage
* Southern Nigeria: 109 studies (47.8%)
* National coverage: 60 studies (26.3%)
* Northern Nigeria: 58 studies (25.4%)
* Not specified: 1 study (0.4%)

### Publication Trends (2014-2024)
The number of MCH studies increased substantially over the decade, from 8 studies in 2014 to 24 studies in 2024, reflecting growing research attention to maternal and child health in Nigeria.

### Research Settings
* Facility-based: 104 studies
* Community-based: 56 studies  
* Both settings: 61 studies
* Not specified: 7 studies

### Funding Sources
* International funding: 112 studies
* No funding disclosure: 63 studies
* Local funding: 6 studies

## Analysis Approach

The project used a structured and transparent approach that included data preparation, validation, and multi-dimensional analysis.

### Data Processing and Cleaning

* Organized 228 studies into a structured dataset with over 20 variables
* Developed a consistent coding system for categorizing limitations
* Applied validation checks to maintain accuracy and consistency
* Cleaned geographic and setting categories for consistent analysis

### Analytical Framework

Thirteen analyses were conducted to examine how limitations appeared across different research dimensions:

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
12. Top 5 limitations temporal trends – evolution of methodological awareness (2014-2024)
13. Limitation co-occurrence – analysis of which limitations frequently appear together

### Technical Implementation

* Implemented in Python using pandas, matplotlib, numpy, and seaborn
* Automated generation of figures for use in academic manuscripts
* Designed a reproducible workflow for transparency and reuse
* Structured code for easy maintenance and future extensions

## Outputs Generated

* Thirteen ready-to-publish visualizations (`outputs/figures/`)
* Clean and documented analysis code (`scripts/clean_analysis.py`)
* Summary tables and insights for manuscript development
* Comprehensive descriptive statistics of the research landscape

### Figure Index
* `01_limitation_categories.png` – Broad limitation categories prevalence
* `02_specific_limitations.png` – Top 10 specific limitation codes
* `03_facility_vs_community.png` – Setting-based comparison
* `04_regional_comparison.png` – North vs. South Nigeria analysis
* `05_trends_over_time.png` – Temporal patterns 2014-2024
* `06_contextual_limitations_trends.png` – Operational challenges over time
* `07_topic_areas.png` – Variation across MCH subfields
* `08_funding_impact.png` – Funding and limitation reporting
* `09_urban_rural.png` – Geographic setting disparities
* `10_multi_site.png` – Study design complexity
* `11_journal_types.png` – Publication venue influence
* `12_top5_limitations_trends.png` – Evolution of top limitations
* `13_limitation_cooccurrence.png` – Limitation clustering patterns

## Repository Structure
scoping-review-mch-nigeria/
├── data/
│ └── raw/
│ └── Extracted_data_v1.csv # Primary dataset (not public)
├── scripts/
│ └── clean_analysis.py # Main analysis pipeline
├── outputs/
│ └── figures/ # Manuscript-ready visualizations
│ ├── 01_limitation_categories.png
│ ├── 02_specific_limitations.png
│ ├── ... (13 figures total)
│ └── 13_limitation_cooccurrence.png
└── README.md # Project documentation

text

**Note:** The full dataset used for this analysis is not included in this repository to protect the copyright and intellectual property of the original studies. The analysis is based on 228 peer-reviewed MCH research articles published between 2014 and 2024.

## Technical Details

### Requirements

Before running the analysis, ensure that the following Python libraries are installed:

* pandas ≥ 1.5.0
* matplotlib ≥ 3.5.0  
* numpy ≥ 1.21.0
* seaborn ≥ 0.11.0

Install required packages using:

```bash
pip install pandas matplotlib numpy seaborn
Running the Analysis
Run the following command in your terminal to reproduce the analysis:

bash
python scripts/clean_analysis.py
The script will execute all 13 analyses and generate the complete set of visualizations in the outputs/figures/ directory.

Dissemination Plans
The findings from this project are being prepared for:

Journal publication in peer-reviewed public health or research methodology outlets

Conference presentations to share insights with the global MCH research community

Stakeholder briefings for Nigerian research institutions, policymakers, and funders

This work aims to contribute to improving research quality, transparency, and capacity building in Nigeria's maternal and child health research ecosystem.

Authors
This repository was developed and maintained by Victor Ekoche Ali, Lead Data Analyst on the Scoping Review team.

Citation
If you use or reference this repository, please cite as:

Ali, V.E. (2025). Scoping Review: Analysis of Reported Limitations in Nigerian Maternal and Child Health Research (2014–2024). GitHub Repository. https://github.com/Ekoche1/scoping-review-mch-nigeria

License
This repository is available for academic and research purposes. Please cite appropriately if the code or analytical framework is used or adapted.

Summary
This project demonstrates how structured data analysis can help identify recurring research challenges and guide improvements in study design, reporting, and evidence quality. By highlighting common methodological and contextual limitations, it contributes to building stronger and more transparent maternal and child health research in Nigeria. The comprehensive analysis of 228 studies provides valuable insights for researchers, funders, and policymakers working to enhance the quality and impact of MCH research in Nigeria and similar contexts.