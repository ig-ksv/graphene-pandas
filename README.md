# graphene-pandas(under developing)

## Installation

For instaling graphene-pandas, just run this command in your shell

```bash
not ready 
```

## Examples

To create a GraphQL schema for it you simply have to write the following:

```python
import graphene
import pandas as pd

from graphene_pandas import DataFrameObjectType

data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000]}
df = pd.DataFrame(test_data)             


class Query(DataFrameObjectType):
    class Meta:
        model = df


schema = graphene.Schema(query=Query)
```

Then you can simply query the schema:

```python
query = '''
    query GrapheneDataFrame {
      Price
      Brand
    }
'''
result = schema.execute(query)
```
```
