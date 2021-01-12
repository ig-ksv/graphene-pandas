import pandas as pd
import graphene

from collections import OrderedDict

from graphene.types.objecttype import ObjectType, ObjectTypeOptions
from graphene.types.utils import yank_fields_from_attrs

from .utils import replace_nan_values_list, replace_nan_values_dict


def convert_field_type(column_type):
    if pd.api.types.is_float_dtype(column_type):
        field_type = graphene.Float
    elif pd.api.types.is_integer_dtype(column_type):
        field_type = graphene.Int
    elif pd.api.types.is_bool_dtype(column_type):
        field_type = graphene.Boolean
    elif pd.api.types.is_datetime64_any_dtype(column_type):
        field_type = graphene.DateTime
    else:
        field_type = graphene.String

    return field_type


def construct_fields(model, exclude_fields=(), only_fields=()):
    fields = OrderedDict()

    for column_name, column_type in model.dtypes.items():
        if column_name in exclude_fields:
            continue
        elif column_name not in only_fields:
            field_type = convert_field_type(column_type)
            fields[column_name] = graphene.Field(field_type)

    return fields


class DataFrameObjectTypeOptions(ObjectTypeOptions):
    model = None
    id = None


class DataFrameObjectType(ObjectType):
    @classmethod
    def __init_subclass_with_meta__(
            cls,
            model=None,
            only_fields=(),
            exclude_fields=(),
            id=None,
            _meta=None,
            **options
    ):
        assert isinstance(model, pd.DataFrame), (
            "You need to pass a valid pandas DataFrame in " '{}.Meta, received "{}".'
        ).format(cls.__name__, model)

        if only_fields and exclude_fields:
            raise ValueError("The options 'only_fields' and 'exclude_fields' cannot be both set on the same type.")

        new_fields = construct_fields(model=model, exclude_fields=exclude_fields, only_fields=only_fields)
        pd_fields = yank_fields_from_attrs(new_fields, _as=graphene.Field, sort=False)

        if not _meta:
            _meta = DataFrameObjectTypeOptions(cls)

        _meta.model = model

        if _meta.fields:
            _meta.fields.update(pd_fields)
        else:
            _meta.fields = pd_fields

        _meta.id = id or "id"

        super(DataFrameObjectType, cls).__init_subclass_with_meta__(_meta=_meta, **options)

    @classmethod
    def get_raw_data(cls, info):
        model = cls._meta.model
        return model

    @classmethod
    def get_all_rows(cls, info):
        model = cls._meta.model
        model_dict = model.to_dict(orient="records")
        return replace_nan_values_list(model_dict)

    @classmethod
    def get_row_int_index(cls, info, index):
        model = cls._meta.model
        model_dict = model.iloc[[index]].to_dict(orient="records")[0]
        return replace_nan_values_dict(model_dict)

    @classmethod
    def get_row_by_label_index(cls, info, index):
        model = cls._meta.model
        model_dict = model.loc[[index]].to_dict(orient="records")[0]
        return replace_nan_values_dict(model_dict)
