import math

import pandas as pd
import graphene

from graphene_pandas import DataFrameObjectType


class TestBasicQueries:
    def _pre_setup(self, df: pd.DataFrame, ex_fields=(), on_fields=()):
        class Records(DataFrameObjectType):
            class Meta:
                model = df
                exclude_fields = ex_fields
                only_fields = on_fields

        class DataFrameQuery(graphene.ObjectType):
            records = graphene.Field(Records, brand=graphene.String(), index=graphene.Int())

            def resolve_records(self, info, index):
                query = Records.get_row_int_index(info, index)
                return query

        self.schema = graphene.Schema(query=DataFrameQuery)

    def test_string_integer_columns(self):
        test_data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
                     "Price": [22000, 25000, 27000, 35000]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        test_index = 1

        query = f"""
            query Test {{
              records(index: {test_index}) {{
                Brand
                Price
              }}
            }}
        """
        result = self.schema.execute(query)

        assert result.data["records"]["Brand"] == test_data["Brand"][test_index]
        assert result.data["records"]["Price"] == test_data["Price"][test_index]

    def test_float_columns(self):
        test_data = {"Price": [0.12, 234.583, 0.00002, 1936292676.7]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        test_index = 1

        query = f"""
                   query Test {{
                     records(index: {test_index}) {{
                       Price
                     }}
                   }}
               """
        result = self.schema.execute(query)

        assert result.data["records"]["Price"] == test_data["Price"][test_index]

    def test_bool_columns(self):
        test_data = {"BoolColumn": [True, False, False, True]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        test_index = 1

        query = f"""
                   query Test {{
                     records(index: {test_index}) {{
                       BoolColumn
                     }}
                   }}
               """
        result = self.schema.execute(query)

        assert result.data["records"]["BoolColumn"] == test_data["BoolColumn"][test_index]

    def test_nan_values(self):
        test_data = {"Price": [0.12, None, 54.0, None]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        test_index = 1

        query = f"""
                   query Test {{
                     records(index: {test_index}) {{
                       Price
                     }}
                   }}
               """
        result = self.schema.execute(query)

        assert result.data["records"]["Price"] == test_data["Price"][test_index]

    def test_date_datetime_values(self):
        from datetime import datetime, date
        test_data = {"Dates": [date(2012, 5, 11), date(2005, 2, 5)],
                     "DateTimes": [datetime(2012, 5, 11, 10, 10), datetime(2005, 2, 5, 12, 30)]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        test_index = 1

        query = f"""
                   query Test {{
                     records(index: {test_index}) {{
                       Dates
                       DateTimes
                     }}
                   }}
               """
        result = self.schema.execute(query)

        assert result.data["records"]["Dates"] == "2005-02-05"
        assert result.data["records"]["DateTimes"] == "2005-02-05T12:30:00"

    def test_exclude_fields(self):
        test_data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
                     "Price": [22000, 25000, 27000, 35000]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df, ex_fields=("Price",))

        test_index = 1

        query = f"""
                    query Test {{
                      records(index: {test_index}) {{
                        Brand
                        Price
                      }}
                    }}
                """
        result = self.schema.execute(query)

        assert result.errors[0].message == 'Cannot query field "Price" on type "Records".'


