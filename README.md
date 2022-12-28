# Labour satellite

This tool unpacks public labour data and rewrites it in a format for the OAASIS project - the Open analysis to address slavery in supply chains (https://www.sydney.edu.au/science/our-research/research-areas/physics/big-data-combatting-modern-slavery.html).

The output format is a 'satellite' account for an environmentally-extended input-output model (EEIO). Currently the OAASIS project is using the GLORIA MRIO model (https://ielab.info/analyse/gloria).

## Using the tool
### The objects directory
`raw`: This directory contains the raw data, unmodified from the source publisher

`concs`: Binary concordance matrices for mapping between classifications

`processed`: Processed data, i.e. the raw data is unpacked into n-d tensors before being written as a satellite vector

`satellite`: Final satellite vectors by year, publisher, and data source

`proxy`: The `root_proxies_by_country.csv` file defines vectors at the root sector level, for each country, which allow disaggregation maps to be constructed. This file is optional, and if it is not present proxies of ones are used instead.

### Data index
The `index.json` file in `\objects\` defines meta for each data source that enables each source to be written as a satellite vector.

```
{"publisher": "ILO",
  "dataset_id": "INJ_FATL_ECO_NB_A_EN",
  "concordance_fname": "ILO_INJ_FATL_ECO_NB_A_EN_22_conc.xlsx",
  "fill_missing": true
  }
```

## Datasets
### ILO data
International Labor Organization datasets (https://ilostat.ilo.org/).

#### Occupational injuries
Cases of fatal occupational injury by economic activity

Dataset ID: INJ_FATL_ECO_NB_A_EN

Unpacked dataset contains 564 records, 12 years data (2009-2020), 81 countries,  source industry resolution: 22

### Shilling
The Shilling et al. dataset represents counts of cases of forced labour by country and sector. In constructing the dataset, it was assumed slavery is most likely to occur in low-skilled labour, such as agriculture. Citation: Shilling, H., Wiedmann, T. & Malik, A. (2021). Modern Slavery Footprints in Global Supply Chains. Journal of Industrial Ecology.

Unpacked dataset contains 140 records, 1 year(s) data (2018-2018), 119 countries, source industry resolution: 57

