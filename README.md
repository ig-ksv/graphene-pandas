[![Build Status](https://travis-ci.com/ig-ksv/graphene-pandas.svg?branch=main)](https://travis-ci.com/ig-ksv/graphene-pandas) [![Coverage Status](https://coveralls.io/repos/github/ig-ksv/graphene-pandas/badge.svg?branch=main)](https://coveralls.io/github/ig-ksv/graphene-pandas?branch=main)

# graphene-pandas(under developing)

## Installation

For instaling graphene-pandas, just run this command in your shell

```bash
pip3 install graphene-pandas(not implemented)
```

## Examples

To create a GraphQL schema for it, you simply have to write the following:

```python
import pandas as pd

import graphene
from graphene_pandas import DataFrameObjectType

data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
        "Price": [22000, 25000, 27000, 35000]}
df = pd.DataFrame(data)


class Records(DataFrameObjectType):
    class Meta:
        model = df
        exclude_fields = ()


class Query(graphene.ObjectType):
    record = graphene.Field(Records, index=graphene.Int())
    records = graphene.List(Records)

    def resolve_record(self, info, index):
        query = Records.get_row_int_index(info, index)
        return query

    def resolve_records(self, info):
        query = Records.get_all_rows(info)
        return query

schema = graphene.Schema(query=Query)

query = """
            query Test {
              record(index: 1) {
                Brand
                Price
              }
              records {
                Brand
                Price
              }
            }
        """

result = graphene.schema.execute(query)
```
```
