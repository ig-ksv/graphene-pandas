import math


def replace_nan_values_dict(query):
    for key, value, in query.items():
        if type(value) is float and math.isnan(value):
            query[key] = None
    return query


def replace_nan_values_list(query):
    for record in query:
        for key, value, in record.items():
            if type(value) is float and math.isnan(value):
                query[key] = None
    return query
