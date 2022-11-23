# Labour satellite

This tool unpacks public labour data and rewrites it in a format for the OAASIS project - the Open analysis to address slavery in supply chains (https://www.sydney.edu.au/science/our-research/research-areas/physics/big-data-combatting-modern-slavery.html).

The output format is a 'satellite' account for an environmentally-extended input-output model (EEIO). Currently the OAASIS project is using the GLORIA MRIO model (https://ielab.info/analyse/gloria).

## objects directory
`raw`: This directory contains the raw data, unmodified from the source publisher

`concs`: Binary concordance matrices for mapping between classifications

`processed`: Processed data, i.e. the raw data is unpacked into n-d tensors before being written as a satellite vector

`satellite`: Final satellite vectors by year, publisher, and data source

`index.json`

## ILO data
International Labor Organization datasets.

### Occupational injuries
Dataset ID: INJ_FATL_ECO_NB_A_EN

Unpacked dataset contains 564 records, 12 years data (2009-2020), 81 countries,  source industry resolution: 22