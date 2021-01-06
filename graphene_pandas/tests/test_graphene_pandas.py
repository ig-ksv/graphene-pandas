import pandas as pd
import numpy as np

from graphene import Schema

from graphene_pandas import DataFrameObjectType


class TestBasicQueries:
    def _pre_setup(self, df: pd.DataFrame, ex_fields=()):
        class DataFrameQuery(DataFrameObjectType):
            class Meta:
                model = df
                exclude_fields = ex_fields

        self.schema = Schema(query=DataFrameQuery)

    def test_string_integer_columns(self):
        test_data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
                     "Price": [22000, 25000, 27000, 35000]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        query = """
            query GrapheneDataFrame {
              Price
              Brand
            }
        """
        result = self.schema.execute(query)
        assert result.data["Brand"] == ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"]
        assert result.data["Price"] == [22000, 25000, 27000, 35000]

    def test_get_default_id_request(self):
        test_data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
                     "Price": [22000, 25000, 27000, 35000]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        query = """
            query GrapheneDataFrame {
              id
            }
        """
        result = self.schema.execute(query)
        assert result.data["id"] == [0, 1, 2, 3]

    def test_float_columns(self):
        test_data = {"Price": [0.12, 234.583, 0.00002, 1936292676.7]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        query = """
            query GrapheneDataFrame {
              Price
            }
        """
        result = self.schema.execute(query)
        assert result.data["Price"] == [0.12, 234.583, 0.00002, 1936292676.7]

    def test_bool_columns(self):
        test_data = {"BoolColumn": [True, False, False, True]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        query = """
            query GrapheneDataFrame {
              BoolColumn
            }
        """
        result = self.schema.execute(query)
        assert result.data["BoolColumn"] == [True, False, False, True]

    def test_nan_values(self):
        test_data = {"Price": [0.12, None, 54.0, None]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        query = """
               query GrapheneDataFrame {
                 Price
               }
           """
        result = self.schema.execute(query)
        assert len(list(filter(lambda x: np.isnan(x), result.data["Price"]))) == 2
        assert len(result.data["Price"]) == 4

    def test_date_datetime_values(self):
        from datetime import datetime, date
        test_data = {"Dates": [date(2012, 5, 11), date(2005, 2, 5)],
                     "DateTimes": [datetime(2012, 5, 11, 10, 10), datetime(2005, 2, 5, 12, 30)]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df)

        query = """
               query GrapheneDataFrame {
                 Dates
                 DateTimes
               }
           """
        result = self.schema.execute(query)
        assert result.data["Dates"] == ["2012-05-11", "2005-02-05"]
        assert result.data["DateTimes"] == ["2012-05-11T10:10:00", "2005-02-05T12:30:00"]

    def test_exclude_fields(self):
        test_data = {"Brand": ["Honda Civic", "Toyota Corolla", "Ford Focus", "Audi A4"],
                     "Price": [22000, 25000, 27000, 35000]}

        test_df = pd.DataFrame(test_data)
        self._pre_setup(test_df, ex_fields=("Price",))

        query = """
            query GrapheneDataFrame {
              Brand
              Price
            }
        """
        result = self.schema.execute(query)
        assert result.errors[0].message == 'Cannot query field "Price" on type "DataFrameQuery".'


