import graphene
import pandas as pd

from fastapi import FastAPI
from starlette.graphql import GraphQLApp

from graphene_pandas import DataFrameObjectType


data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Mazda"],
        "Price": [22000, 25000, 27000, 1234]}
df = pd.DataFrame(data)


class Records(DataFrameObjectType):
    class Meta:
        model = df
        exclude_fields = ()


class Query(graphene.ObjectType):
    record = graphene.Field(Records, brand=graphene.String(), index=graphene.Int())
    records = graphene.List(Records, brand=graphene.String())

    def resolve_record(self, info, index):
        query = Records.get_row_int_index(info, index)
        return query

    def resolve_records(self, info):
        query = Records.get_all_rows(info)
        return query


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))