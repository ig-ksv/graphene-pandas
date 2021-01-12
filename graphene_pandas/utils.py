import math


def replace_nan_values(query):
    for key, value, in query.items():
        if type(value) is float and math.isnan(value):
            query[key] = None
    return query
