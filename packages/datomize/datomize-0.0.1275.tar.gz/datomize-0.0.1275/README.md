Welcome to Datomize Python SDK
==============================

Datomize is a Data-Driven Solution to machine learning. Datomize augments source data with synthetic data of exceptional quality, and can be used to generate synthetic replicas, optimize training data with balanced and richer data, and address the data bias challenge.

# Getting Started

## Getting your application user & password

In order to use the Datomize Python SDK client, you first need to register the Datomize solution. Once registering Datomize, you will be provided with ``username`` and ``password``, which get passed to ``datomize.Datomizer()`` when starting your application.

Please register the Datomize solution on Datomize [Registration](https://app.datomize.com/#/dcs-on-boarding-page).

## Installation

```shell
pip install datomize
```

## Important links

- [Documentation](https://datomize.github.io/datomizeSDK)

### Usage Example
```python
# Import relevant packages
from datomizer import Datomizer, DatoMapper, DatoTrainer, DatoGenerator
from sklearn.datasets import load_iris 
import pandas as pd

# load input data:
data=load_iris(return_X_y=False,as_frame=True)
df = pd.concat([data.data,data.target],axis=1)

# Create a Datomizer with your credentials:
datomizer = Datomizer(username=username, password=password)

# Create a DatoMapper and analyze the data structure:
mapper = DatoMapper(datomizer)
mapper.discover(df=df)

# Create a DatoTrainer and train the generative model:
trainer = DatoTrainer(mapper)
trainer.train()

# Create a DatoGenerator and generate output data:
generator = DatoGenerator(trainer)
generator.generate()
dato_df = pd.read_csv(generator.get_generated_data_csv())
```

### Async Usage Example
```python
from datomizer import Datomizer, DatoMapper, DatoTrainer, DatoGenerator
 
datomizer = Datomizer(username=username, password=password)
  
mapper = DatoMapper(datomizer)
mapper.discover(df=df, title="Some Title", wait=False)
...do something...
mapper.wait()
 
trainer = DatoTrainer(mapper)
trainer.train(wait=False)
...do something...
trainer.wait()

generator = DatoGenerator(trainer)
generator.generate(wait=False)
...do something...
generator.wait()
 
dato_df = pd.read_csv(generator.get_generated_data_csv())
```
