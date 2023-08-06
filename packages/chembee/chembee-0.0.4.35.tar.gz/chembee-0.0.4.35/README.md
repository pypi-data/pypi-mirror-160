# Chembee

## Why

To accelerate the shift to a sustainable, lean, and demand-driven chemical industry, we at sail.black needed a package to draft microservices fast and reliably. The `chembee` package abstracts the development of modules in the pipeline envisioned in 2020 for a rapid prototyping software evaluating sustainable chemicals (compare: https://www.researchgate.net/project/Lean-Drug-Development).

## What

`Chembee` is a modelling kit automatizing the first step of the MLOps value pipeline for a given dataset. The perspective is not algorithm-specific but rather 
dataset-specific. The package therefore operates data-centric as in contrast to `scikit-learn` that is algorithm centric. 

In the end, data creates value. The package shall help finding the best treatment for a given dataset fast. Automatizing rapid prototyping for environmental degradation modelling and other endpoints, the package merges CADD and Environmental Sciences. 

Models crafted with and by `chembee` must follow the REACH and OECD guidelines for QSAR models replacing experiments for environmental and pharmaceutical endpoints. Therefore, the `chembee_actions` module provides functionality to comply with the `REACH` and `OECD` standards. 

The goal of `chembee` is thus to provide methods to create explainable, compliant, and production-ready, QSAR models for use in microservices fast.

### Software Pattern

The software pattern is as follows: 

![SOLID Pattern](solid_pattern_white.png)

And follows SOLID principles. Still, not yet proven in the field, the data preparation might be seen as an action, too. The perspective of seeing the 
data preparation as part of the actions module, would further abstract the software pattern and is worth a thought for future releases. Do you have any ideas? Participate in our discussions!

### Merging CADD and Environmental Sciences

A primer of what the synthesis of Environmental Sciences and CADD can achieve:

![Distribution Dataset](tests/plots/plots.png)

## Requirements 


# Installation 
```
pip install chembee
```

# Visuals 
Get to know your data with especially polar charts. 

# Example Biodegradability
## Is Ready Biodegrable
![Polar Chart](tests/plots/BiodegPolar.png)
## Is Not Ready Biodegradable
![Polar Chart](tests/plots/NBiodegPolar.png)

Both pictures show clearly that the Lipinski rule of five plays a significant role in the rady biodegradability of a chemical compound according to the OECD Guideline 301. It can be concluded that ready biodegradable compounds follow the Lipinski rule of five more closely than non-biodegradable compounds. 


# Testing

As the workload for testing is quite heavy, we are evaluating `pytest.fixture`

You should also check coverage in your CI/CD

```
pytest --cov tests/
```

# References 

1. Ruiz-Moreno, A. J., Reyes-Romero, A., Dömling, A., & Velasco-Velázquez, M. A. (2021). In silico design and selection of new tetrahydroisoquinoline-based CD44 antagonist candidates. Molecules (Basel, Switzerland), 26(7), 1877.
2. Lunghini F, Marcou G, Gantzer P, Azam P, Horvath D, Van Miert E, Varnek A. 2020 Modelling of ready biodegradability based on combined public and industrial data sources. SAR QSAR Environ. Res. 31, 171–186. (doi:10.1080/1062936X.2019.1697360)
3. Elsayad AM, Nassef AM, Al-Dhaifallah M, Elsayad KA. 2020 Classification of biodegradable substances using balanced random trees and boosted c5.0 decision trees. Int. J. Environ. Res. Public Health 17, 1–22. (doi:10.3390/ijerph17249322)

# How to cite

Before there is a publication, you can always cite the Git. 




