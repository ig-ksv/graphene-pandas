[![Build Status](https://travis-ci.com/ig-ksv/graphene-pandas.svg?branch=main)](https://travis-ci.com/ig-ksv/graphene-pandas) [![Coverage Status](https://coveralls.io/repos/github/ig-ksv/graphene-pandas/badge.svg?branch=main)](https://coveralls.io/github/ig-ksv/graphene-pandas?branch=main)

# graphene-pandas(under developing)

## Installation

For instaling graphene-pandas, just run this command in your shell

```bash
pip3 install graphene-pandas
```

## Examples

To create a GraphQL schema for it you simply have to write the following:

```python
import pandas as pd

from graphene import Schema
from graphene_pandas import DataFrameObjectType

data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000]}
df = pd.DataFrame(data)


class Query(DataFrameObjectType):
    class Meta:
        model = df
        exclude_fields = ()


schema = Schema(query=Query)

#Then you can simply query the schema:

query = '''
    query GrapheneDataFrame {
      Price
      Brand
    }
'''
result = schema.execute(query)
```
```
