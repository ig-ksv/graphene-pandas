import  pandas as pd

def get_unbound_function(func):
    if not getattr(func, "__self__", True):
        return func.__func__
    return func


def get_custom_resolver(obj_type, orm_field_name):
    resolver = getattr(obj_type, 'resolve_{}'.format(orm_field_name), None)
    if resolver:
        return get_unbound_function(resolver)
    return None


def get_attr_resolver(obj_type: pd.DataFrame):
    return lambda root, info: obj_type[info.field_name]


def get_default_id_resolver(obj_type: pd.DataFrame):
    return lambda root, info: obj_type.index.values