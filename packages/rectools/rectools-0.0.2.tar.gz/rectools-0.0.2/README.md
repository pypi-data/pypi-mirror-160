# RecTools

RecTools is an easy-to-use Python library which makes the process of building recommendation systems easier, 
faster and more structured than ever before.
It includes built in toolkits for data processing and metrics calculation, 
a variety of recommender models, some wrappers for already existing implementations of popular algorithms 
and model selection framework.
The aim is to collect ready-to-use solutions and best practices in one place to make processes 
of creating your first MVP and deploying model to production as fast and easy as possible.

RecTools allows to easily work with dense and sparse features.
It features such basic models as ones based on random suggestions or popularity and more advanced ones, e.g. LightFM.
It also contains a wide variety of metrics to choose from to better suit recommender system to your needs.

For more details, see the [Documentation](https://strategic.pages.mts.ru/esaul/mars/).

## Get started
```python
import pandas as pd
from implicit.nearest_neighbours import TFIDFRecommender
    
from rectools import Columns
from rectools.dataset import Dataset
from rectools.models import ImplicitItemKNNWrapperModel

# Read the data
ratings = pd.read_csv(
    "ml-1m/ratings.dat", 
    sep="::",
    engine="python",  # Because of 2-chars separators
    header=None,
    names=[Columns.User, Columns.Item, Columns.Weight, Columns.Datetime],
)
    
# Create dataset
dataset = Dataset.construct(ratings)
    
# Fit model
model = ImplicitItemKNNWrapperModel(TFIDFRecommender(K=10))
model.fit(dataset)

# Make recommendations
recos = model.recommend(
    users=ratings[Columns.User].unique(),
    dataset=dataset,
    k=10,
    filter_viewed=True,
)
```

## Installation

RecTools is on PyPI, so you can use `pip` to install it.
```
pip install rectools
```

## CICD

На всех ветках запускается stage - test и для TAG build_and_publish_pip_package-->deploy_docs

## Contribution

To install all requirements run
```
make install
```
You must have `python3` and `virtualenv` installed.

For autoformatting run 
```
make autoformat
```

For linters check run 
```
make lint
```

For tests run 
```
make test
```

For coverage run 
```
make coverage
```

To remove virtual environment run
```
make clean
```
